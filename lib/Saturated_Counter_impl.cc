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
#include "Saturated_Counter_impl.h"

namespace gr {
  namespace amateur {

    Saturated_Counter::sptr
    Saturated_Counter::make(const float satLow, const float satHigh)
    {
      return gnuradio::get_initial_sptr
        (new Saturated_Counter_impl(satLow, satHigh));
    }

    /*
     * The private constructor
     */
    Saturated_Counter_impl::Saturated_Counter_impl(const float satLow, const float satHigh)
      : gr::sync_block("Saturated_Counter",
              gr::io_signature::make(1, 1, sizeof(float)),
              gr::io_signature::make(1, 1, sizeof(float)))
    {
        d_satLow  = satLow;
        d_satHigh = satHigh;
        d_accum   = 0.0f;
    }

    /*
     * Our virtual destructor.
     */
    Saturated_Counter_impl::~Saturated_Counter_impl()
    {
    }

    int
    Saturated_Counter_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      const float *in = (const float *) input_items[0];
      float *out = (float *) output_items[0];

      for (int k = 0; k < noutput_items; k++)
      {
          d_accum = d_accum + in[k];
          d_accum = (d_accum < d_satLow)  ? d_satLow  : d_accum;
          d_accum = (d_accum > d_satHigh) ? d_satHigh : d_accum;
          out[k]  = d_accum;
      }

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace amateur */
} /* namespace gr */

