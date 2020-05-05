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

#ifndef INCLUDED_AMATEUR_BURST_STAGER_IMPL_H
#define INCLUDED_AMATEUR_BURST_STAGER_IMPL_H

#include <amateur/Burst_Stager.h>

#include <gnuradio/filter/firdes.h>
#include <gnuradio/filter/fir_filter.h>

namespace gr {
  namespace amateur {

    class Burst_Stager_impl : public Burst_Stager
    {
     private:
         std::vector<gr_complex> d_buffer;
         std::vector<gr_complex> d_resampled;
         unsigned int d_maxDepth;
         unsigned int d_burstLen;
         pmt::pmt_t   d_burstTag;

         gr::thread::mutex d_lock;
         float d_step;
         std::vector<float> d_taps;
         std::vector<gr::filter::kernel::fir_filter_ccf*> d_filt;
         std::vector<gr::filter::kernel::fir_filter_ccf*> d_dfilt;

         void createResampler();
         void resample();
         void send();

     public:
      Burst_Stager_impl(const std::string &lengthTag, const unsigned int initDepth, const int maxDepth, const float rate);
      ~Burst_Stager_impl();

      void set_rate(const float rate);

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace amateur
} // namespace gr

#endif /* INCLUDED_AMATEUR_BURST_STAGER_IMPL_H */

