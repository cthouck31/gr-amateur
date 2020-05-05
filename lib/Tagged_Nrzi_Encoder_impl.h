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

#ifndef INCLUDED_AMATEUR_TAGGED_NRZI_ENCODER_IMPL_H
#define INCLUDED_AMATEUR_TAGGED_NRZI_ENCODER_IMPL_H

#include <amateur/Tagged_Nrzi_Encoder.h>

namespace gr {
  namespace amateur {

    class Tagged_Nrzi_Encoder_impl : public Tagged_Nrzi_Encoder
    {
     private:
         unsigned char d_init;
         unsigned char d_delay;
         pmt::pmt_t         d_frameTag;

     public:
      Tagged_Nrzi_Encoder_impl(const std::string frameTag, const unsigned int init);
      ~Tagged_Nrzi_Encoder_impl();

      // Where all the action really happens
      int work(int noutput_items,
         gr_vector_const_void_star &input_items,
         gr_vector_void_star &output_items);
    };

  } // namespace amateur
} // namespace gr

#endif /* INCLUDED_AMATEUR_TAGGED_NRZI_ENCODER_IMPL_H */

