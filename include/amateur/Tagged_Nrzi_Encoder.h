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


#ifndef INCLUDED_AMATEUR_TAGGED_NRZI_ENCODER_H
#define INCLUDED_AMATEUR_TAGGED_NRZI_ENCODER_H

#include <amateur/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace amateur {

    /*!
     * \brief <+description of block+>
     * \ingroup amateur
     *
     */
    class AMATEUR_API Tagged_Nrzi_Encoder : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<Tagged_Nrzi_Encoder> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of amateur::Tagged_Nrzi_Encoder.
       *
       * To avoid accidental use of raw pointers, amateur::Tagged_Nrzi_Encoder's
       * constructor is in a private implementation
       * class. amateur::Tagged_Nrzi_Encoder::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::string frameTag, const unsigned int init = 0x1);
    };

  } // namespace amateur
} // namespace gr

#endif /* INCLUDED_AMATEUR_TAGGED_NRZI_ENCODER_H */

