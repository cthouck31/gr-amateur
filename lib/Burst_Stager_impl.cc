/* -*- c++ -*- */
/*
 * Copyright 2020 <+YOU OR YOUR COMPANY+>.
 *
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <gnuradio/io_signature.h>
#include <volk/volk.h>
#include "Burst_Stager_impl.h"

namespace gr {
  namespace amateur {

    Burst_Stager::sptr
    Burst_Stager::make(const std::string &lengthTag, const unsigned int initDepth, const int maxDepth, const float rate)
    {
      return gnuradio::get_initial_sptr
        (new Burst_Stager_impl(lengthTag, initDepth, maxDepth, rate));
    }

    /*
     * The private constructor
     */
    Burst_Stager_impl::Burst_Stager_impl(const std::string &lengthTag, const unsigned int initDepth, const int maxDepth, const float rate)
      : gr::sync_block("Burst_Stager",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(0, 0, 0)),
        d_maxDepth((unsigned int)maxDepth),
        d_burstLen(0),
        d_burstTag(pmt::intern(lengthTag))
    {
        d_buffer.reserve(initDepth);
        message_port_register_out(pmt::intern("out"));

        createResampler();
        set_rate(rate);
    }

    /*
     * Our virtual destructor.
     */
    Burst_Stager_impl::~Burst_Stager_impl()
    {
        unsigned int k;
        for (k = 0; k < d_filt.size(); k++)
        {
            delete d_filt[k];
            delete d_dfilt[k];
        }
    };

    void
    Burst_Stager_impl::createResampler()
    {
        unsigned int k, m, j;
        std::vector<float> buffer;
        std::vector<float> dbuffer;
        const unsigned int numPaths = 64;
        unsigned int tapsPerPath;
        // Create taps.
        std::vector<float> dtaps;
        d_taps =
            gr::filter::firdes::low_pass_2(numPaths,
                                           numPaths,
                                           0.5f,
                                           0.125f,
                                           70.0f,
                                           gr::filter::firdes::WIN_BLACKMAN_HARRIS);
        tapsPerPath = (d_taps.size()+numPaths-1) / numPaths;

        // Create derivative taps.
        dtaps = d_taps;
        buffer.insert(buffer.begin(), 3, 0);
        for (k = 0; k < d_taps.size(); k++)
        {
            buffer.insert(buffer.begin(), d_taps[k]);
            buffer.pop_back();
            dtaps[k] = 0.5f*buffer.front() - 0.5f*buffer.back();
        }
        buffer.insert(buffer.begin(), 0);
        buffer.pop_back();
        dtaps.push_back(0.5f*buffer.front() - 0.5f*buffer.back());
        dtaps.erase(dtaps.begin(), dtaps.begin()+1);

        // Create polyphase filters.
        d_filt  = std::vector<gr::filter::kernel::fir_filter_ccf*>(numPaths);
        d_dfilt = std::vector<gr::filter::kernel::fir_filter_ccf*>(numPaths);
        for (k = 0; k < numPaths; k++)
        {
            buffer.clear();
            dbuffer.clear();
            for (m = k; m < d_taps.size(); m += numPaths)
            {
                buffer.push_back(d_taps[m]);
                dbuffer.push_back(dtaps[m]);
            }
            d_filt[k]  = new gr::filter::kernel::fir_filter_ccf(1, buffer);
            d_dfilt[k] = new gr::filter::kernel::fir_filter_ccf(1, dbuffer);
        }

        set_rate(1.0f);
    };

    void
    Burst_Stager_impl::set_rate(const float rate)
    {
        gr::thread::scoped_lock lock(d_lock);

        d_step = (1.0f / rate) * d_filt.size();
    };

    void
    Burst_Stager_impl::resample()
    {
        unsigned int k;
        unsigned int l;
        unsigned int path;
        unsigned int len;
        float d_accum, accum, frac;
        gr_complex m, b;
        gr::filter::kernel::fir_filter_ccf *filt, *dfilt;
        unsigned int numOut;
        const unsigned int d_numPaths = d_filt.size();
        const unsigned int d_tapsPerPath = d_filt.front()->taps().size();
        const float d_rate = d_numPaths / d_step;
        std::vector<gr_complex> d_delay(d_tapsPerPath, 0);

        // Pad w/ zeros (flushes delay).
        d_buffer.insert(d_buffer.begin(), d_tapsPerPath, 0);

        // Reserve space for burst.
        numOut = (unsigned int)ceilf(d_rate * d_buffer.size());
        d_resampled.clear();
        d_resampled.insert(d_resampled.begin(), numOut, 0);

        gr::thread::scoped_lock lock(d_lock);

        // Resample.
        d_accum = 0.0f;
        l = 0;
        for (k = 0; k < d_buffer.size(); k++)
        {
//            d_delay.push_back(d_buffer[k]);
//            d_delay.erase(d_delay.begin(), d_delay.begin()+1);
            d_delay.insert(d_delay.begin(), d_buffer[k]);
            d_delay.pop_back();
            while (d_accum < d_numPaths)
            {
                accum    = d_accum - d_numPaths*floor(d_accum / d_numPaths);
                path     = (unsigned int)accum;
                frac     = accum - path;
                filt     = d_filt[path];
                dfilt    = d_dfilt[path];

//                d_resampled[l++] = \
//                    filt->filter(&d_delay[0]) + \
//                    dfilt->filter(&d_delay[0])*frac;

                volk_32fc_32f_dot_prod_32fc_u(&b, &d_delay[0], &filt->taps()[0], filt->taps().size());
                volk_32fc_32f_dot_prod_32fc_u(&m, &d_delay[0], &dfilt->taps()[0], dfilt->taps().size());
                d_resampled[l++] = m*frac + b;

                d_accum += d_step;
            }
            d_accum -= d_numPaths;
        }

        // Clear burst staging.
        d_buffer.clear();
        d_burstLen = 0;
    };

    void
    Burst_Stager_impl::send()
    {
        pmt::pmt_t msg;
        if (d_resampled.empty())
        {
            return;
        }

//        std::cout << "Sending " << d_resampled.size() << std::endl;

        // Construct message.
        msg = pmt::cons(pmt::PMT_NIL,
                        pmt::init_c32vector(d_resampled.size(),
                                            d_resampled));
        message_port_pub(pmt::intern("out"), msg);

        // Clear resampled output.
        d_resampled.clear();
    };

    int
    Burst_Stager_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      unsigned int burstLen;
      unsigned int num_consumed = 0;
      unsigned int numItems;
      pmt::pmt_t msg;
      std::vector<tag_t> tags;
      const gr_complex *in = (const gr_complex *) input_items[0];

      // Get all length tags.
      get_tags_in_range(tags,
                        0,
                        nitems_read(0),
                        nitems_read(0)+noutput_items,
                        d_burstTag);

      // Process samples until no more exist.
      while (num_consumed < noutput_items)
      {
          // Gather any remaining samples.
          numItems = std::min((unsigned int)noutput_items - num_consumed,
                              d_burstLen - (unsigned int)d_buffer.size());
          if (numItems > 0)
          {
              // Add remaining samples to buffer.
              d_buffer.insert(d_buffer.end(),
                              in + num_consumed,
                              in + num_consumed + numItems);

              // Check if burst is fully staged and forward it.
              if (d_burstLen == d_buffer.size())
              {
                  resample();
                  send();
              }
          }
          num_consumed += numItems;

          // Check if all samples were processed.
          //
          // NOTE: This will ignore any additional flags that
          // occur during a burst. Long bursts will lock the
          // staging block until completed.
          if (num_consumed >= noutput_items)
          {
              continue;
          }

          // Check for new tag.
          if (!tags.empty())
          {
              // Extract new burst length.
              if (pmt::is_integer(tags.front().value))
              {
                  burstLen = pmt::to_long(tags.front().value);
                  // Validate that it fits in the maximum buffer size.
                  if (burstLen <= d_maxDepth)
                  {
                      d_burstLen = burstLen;
                      // Compute new offset (effectively consumes samples up
                      // to point of new burst).
                      num_consumed = tags.front().offset-nitems_read(0);
                  }
                  else
                  {
                      std::cerr << "Requested burst length of " << burstLen
                                << " is larger than maximum of " << d_maxDepth
                                << std::endl;
                  }
              }
              else
              {
                  // Ignore invalid tags.
              }
              // Process tag.
              tags.erase(tags.begin());
          }
          else
          {
              // Finish consuming input samples.
              num_consumed = noutput_items;
          }
      }

      // Tell runtime system how many output items we produced.
      return num_consumed;
    }

  } /* namespace amateur */
} /* namespace gr */

