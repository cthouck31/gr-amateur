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

#include <cmath>
#include <exception>
#include <gnuradio/io_signature.h>
#include <gnuradio/filter/firdes.h>
#include <gnuradio/math.h>
#include <gnuradio/fxpt.h>
#include "Burst_Afsk_Modulator_impl.h"

namespace gr {
  namespace amateur {

    Burst_Afsk_Modulator::sptr
    Burst_Afsk_Modulator::make(const std::string &lengthTag, const float symRate, const float markFreq, const float spaceFreq, const unsigned int sps, const float rrcAlpha, const unsigned int rrcSyms)
    {
      return gnuradio::get_initial_sptr
        (new Burst_Afsk_Modulator_impl(lengthTag, symRate, markFreq, spaceFreq, sps, rrcAlpha, rrcSyms));
    }

    /*
     * The private constructor
     */
    Burst_Afsk_Modulator_impl::Burst_Afsk_Modulator_impl(const std::string &lengthTag, const float symRate, const float markFreq, const float spaceFreq, const unsigned int sps, const float rrcAlpha, const unsigned int rrcSyms)
      : gr::sync_block("Burst_Afsk_Modulator",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(float))),
        d_frameTag(pmt::intern(lengthTag)),
        d_baudRate(symRate),
        d_sps(sps),
        d_pulseShape(gr::filter::firdes::root_raised_cosine(sps,
                                                            sps,
                                                            1.0f,
                                                            rrcAlpha,
                                                            2*rrcSyms*sps+1)),
        d_pfb(sps, d_pulseShape, 1),
        d_rrcAlpha(rrcAlpha),
        d_rrcSyms(rrcSyms),
        d_newBurst(0)
    {
        unsigned int k;

        // Map mark/space frequencies.
        if (markFreq > (d_sps*d_baudRate/2.0f))
        {
            throw std::runtime_error("Mark frequency must be < sample rate.");
        }
        if (spaceFreq > (d_sps*d_baudRate/2.0f))
        {
            throw std::runtime_error("Space frequency must be < sample rate.");
        }
        // Space (0).
        d_freqMap.push_back(spaceFreq / (d_sps*d_baudRate));
        // Mark (1).
        d_freqMap.push_back(markFreq  / (d_sps*d_baudRate));

        // Scale taps (incorporates sensivity scaling).
        for (k = 0; k < d_pulseShape.size(); k++)
        {
            d_pulseShape[k] = d_pulseShape[k] * 2.0f * M_PI;
        }
        d_pfb.set_taps(d_pulseShape);

        set_alpha(d_rrcAlpha);

        // Input messages (bytes).
        message_port_register_in(pmt::intern("in"));
        set_msg_handler(pmt::intern("in"),
                        boost::bind(&Burst_Afsk_Modulator_impl::_handleMessage,
                                    this, _1));
    }

    /*
     * Our virtual destructor.
     */
    Burst_Afsk_Modulator_impl::~Burst_Afsk_Modulator_impl()
    {
    }

    void
    Burst_Afsk_Modulator_impl::set_alpha(const float alpha)
    {
        unsigned int k;
        gr::thread::scoped_lock lock(d_tapLock);

        if (alpha > 0)
        {
            d_pulseShape = gr::filter::firdes::root_raised_cosine(d_sps,
                                                                  d_sps,
                                                                  1.0f,
                                                                  alpha,
                                                                  2*d_rrcSyms*d_sps+1);
        }
        else
        {
            d_pulseShape = std::vector<float>(d_sps, 1.0f);
        }
        // Scale taps (incorporates sensivity scaling).
        for (k = 0; k < d_pulseShape.size(); k++)
        {
            d_pulseShape[k] = d_pulseShape[k] * 2.0f * M_PI;
        }
        d_pfb.set_taps(d_pulseShape);
    };

    void
    Burst_Afsk_Modulator_impl::_handleMessage(pmt::pmt_t msg)
    {
      unsigned int j, k, l;
      float accum;
      float phi, re, im;
      int32_t idx;
      std::vector<uint8_t> dataBits;
      std::vector<std::vector<float> > taps;

      // Check message type.
      pmt::pmt_t value = pmt::cdr(msg);
      if (!pmt::is_u8vector(value))
      {
          std::cerr << "Invalid input type." << std::endl;
          return;
      }

      // Get bits.
      dataBits = pmt::u8vector_elements(value);
      if (dataBits.empty())
      {
          std::cerr << "Empty data vector." << std::endl;
          return;
      }

      // Process input message.

      // Unpack bits and map to mark/space.
      d_work.clear();
      d_work.insert(d_work.begin(), dataBits.size(), 0);
      for (k = 0; k < dataBits.size(); k++)
      {
          d_work[k] = d_freqMap[dataBits[k] & 0x01];
      }

      gr::thread::scoped_lock lock(d_tapLock);

      // Perform pulse shaping.
      taps = d_pfb.taps();
      d_buffer.clear();
      d_buffer.insert(d_buffer.begin(), taps.front().size(), 0);
      d_samples.clear();
      d_samples.insert(d_samples.begin(), taps.size()*d_work.size(), 0);
      for (k = 0; k < d_work.size(); k++)
      {
          d_buffer.insert(d_buffer.begin(), d_work[k]);
          d_buffer.pop_back();
          for (l = 0; l < taps.size(); l++)
          {
              accum = 0.0f;
              for (j = 0; j < taps[l].size(); j++)
              {
                  accum = accum + taps[l][j]*d_buffer[j];
              }
              d_samples[d_sps*k+l] = accum;
          }
      }
      // Flush filter.
      for (k = 0; k < d_rrcSyms; k++)
      {
          d_buffer.insert(d_buffer.begin(), 0);
          d_buffer.pop_back();
          for (l = 0; l < taps.size(); l++)
          {
              accum = 0.0f;
              for (j = 0; j < taps[l].size(); j++)
              {
                  accum = accum + taps[l][j]*d_buffer[j];
              }
              d_samples.push_back(accum);
          }
      }
      // Remove initial delay.
//      d_samples.erase(d_samples.begin(),
//                      d_samples.begin()+d_pulseShape.size()/2);

      // Frequency modulation.
      phi = 0.0f;
      for (k = 0; k < d_samples.size(); k++)
      {
          // Phase accumulator.
          phi = phi + d_samples[k];
          // Wrap [-pi, pi)
          phi = std::fmod(phi+M_PI, 2.0f*M_PI) - M_PI;
          idx = gr::fxpt::float_to_fixed(phi);
          gr::fxpt::sincos(idx, &im, &re);
          d_samples[k] = re;
      }

      // Inject into stream for transmission.
      gr::thread::scoped_lock flock(d_lock);
      d_newBurst = 1;
      d_fifo.insert(d_fifo.end(),
                    d_samples.begin(),
                    d_samples.begin() + d_samples.size());
    };

    int
    Burst_Afsk_Modulator_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      tag_t tag;
      unsigned int ninsert = 0;
      float *out = (float *) output_items[0];

      // Lock mutex.
      gr::thread::scoped_lock lock(d_lock);

      if (d_fifo.empty())
      {
          // Insert zeros.
          memset(out, 0, sizeof(float)*noutput_items);
//          usleep((unsigned int)(0.5*(noutput_items/(d_sps*d_baudRate))*1000000));
      }
      else
      {
          // Insert as many samples as possible.
          ninsert = std::min((unsigned int)noutput_items,
                             (unsigned int)d_fifo.size());
          memcpy(out, &d_fifo[0], ninsert*sizeof(float));
          memset(out+ninsert, 0, sizeof(float)*(noutput_items-ninsert));

          // Add new tag if necessary.
          if (d_newBurst)
          {
              tag.offset = nitems_written(0);
              tag.srcid  = pmt::intern("burst_afsk_modulator");
              tag.key    = d_frameTag;
              tag.value  = pmt::from_long(d_fifo.size());
              add_item_tag(0, tag);

              d_newBurst = 0;
          }

          // Remove from the FIFO.
          d_fifo.erase(d_fifo.begin(), d_fifo.begin()+ninsert);
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace amateur */
} /* namespace gr */

