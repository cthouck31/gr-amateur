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

#ifndef INCLUDED_AMATEUR_BURST_AFSK_MODULATOR_IMPL_H
#define INCLUDED_AMATEUR_BURST_AFSK_MODULATOR_IMPL_H

#include <amateur/Burst_Afsk_Modulator.h>

#include <gnuradio/filter/polyphase_filterbank.h>

namespace gr {
  namespace amateur {

    class Burst_Afsk_Modulator_impl : public Burst_Afsk_Modulator
    {
     private:
         // Frame tag.
         pmt::pmt_t d_frameTag;
         // Mark & space frequencies.
         std::vector<float> d_freqMap;
         // Baud rate.
         float d_baudRate;
         // Samples per symbol (out).
         unsigned int d_sps;
         // Pulse shape taps.
         float d_rrcAlpha;
         unsigned int d_rrcSyms;
         std::vector<float> d_pulseShape;
         // Polyphase interpolator.
         gr::thread::mutex d_tapLock;
         gr::filter::kernel::polyphase_filterbank d_pfb;
         // Output FIFO.
         gr::thread::mutex d_lock;
         bool d_newBurst;
         std::vector<float> d_fifo;

         void _handleMessage(pmt::pmt_t &msg);

         // Processing variables.
         std::vector<float> d_work;
         std::vector<float> d_buffer;
         std::vector<float> d_samples;

     public:
      Burst_Afsk_Modulator_impl(const std::string &lengthTag, const float symRate, const float markFreq, const float spaceFreq, const unsigned int sps, const float rrcAlpha, const unsigned int rrcSyms);
      ~Burst_Afsk_Modulator_impl();

      void set_alpha(const float alpha);

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace amateur
} // namespace gr

#endif /* INCLUDED_AMATEUR_BURST_AFSK_MODULATOR_IMPL_H */

