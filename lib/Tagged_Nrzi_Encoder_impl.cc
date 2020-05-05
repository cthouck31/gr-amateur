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
#include "Tagged_Nrzi_Encoder_impl.h"

namespace gr {
  namespace amateur {

    Tagged_Nrzi_Encoder::sptr
    Tagged_Nrzi_Encoder::make(const std::string frameTag, const unsigned int init)
    {
      return gnuradio::get_initial_sptr
        (new Tagged_Nrzi_Encoder_impl(frameTag, init));
    }

    /*
     * The private constructor
     */
    Tagged_Nrzi_Encoder_impl::Tagged_Nrzi_Encoder_impl(const std::string frameTag, const unsigned int init)
      : gr::sync_block("Tagged_Nrzi_Encoder",
              gr::io_signature::make(1, 1, sizeof(unsigned char)),
              gr::io_signature::make(1, 1, sizeof(unsigned char)))
    {
        d_init     = init;
        d_frameTag = pmt::intern(frameTag);
        d_delay    = !d_init;
    }

    /*
     * Our virtual destructor.
     */
    Tagged_Nrzi_Encoder_impl::~Tagged_Nrzi_Encoder_impl()
    {
    }

    int
    Tagged_Nrzi_Encoder_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      std::vector<tag_t> tags;
      unsigned int k;
      unsigned int lastIdx;
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out      = (unsigned char *) output_items[0];

      // Get all frame tags in range (ordered by scheduler).
      get_tags_in_range(tags,
                        0,
                        nitems_read(0),
                        nitems_read(0)+noutput_items,
                        d_frameTag);

      // Calculate number of old items to process.
      lastIdx = noutput_items;
      if (!tags.empty())
      {
          lastIdx = tags.front().offset - nitems_read(0);
      }

      // Perform differential encoding (w/ inversion).
      for (k = 0; k < lastIdx; k++)
      {
        d_delay = d_delay ^ (!in[k]);
        out[k]  = !d_delay;
      }

      // Process all tags.
      while (!tags.empty())
      {
          tags.erase(tags.begin());
          lastIdx = noutput_items;
          if (!tags.empty())
          {
            lastIdx = tags.front().offset - nitems_read(0);
          }

          // Reset initial value.
          d_delay = !d_init;

          // Perform differential encoding (w/ inversion).
          for (; k < lastIdx; k++)
          {
            d_delay = d_delay ^ (!in[k]);
            out[k]  = !d_delay;
          }
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace amateur */
} /* namespace gr */

