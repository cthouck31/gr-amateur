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


#ifndef INCLUDED_AMATEUR_BURST_AFSK_MODULATOR_H
#define INCLUDED_AMATEUR_BURST_AFSK_MODULATOR_H

#include <amateur/api.h>
#include <gnuradio/sync_block.h>

namespace gr {
  namespace amateur {

    /*!
     * \brief <+description of block+>
     * \ingroup amateur
     *
     */
    class AMATEUR_API Burst_Afsk_Modulator : virtual public gr::sync_block
    {
     public:
      typedef boost::shared_ptr<Burst_Afsk_Modulator> sptr;

      /*!
       * \brief Return a shared_ptr to a new instance of amateur::Burst_Afsk_Modulator.
       *
       * To avoid accidental use of raw pointers, amateur::Burst_Afsk_Modulator's
       * constructor is in a private implementation
       * class. amateur::Burst_Afsk_Modulator::make is the public interface for
       * creating new instances.
       */
      static sptr make(const std::string &lengthTag, const float symRate = 1.0f, const float markFreq = 2200.0f, const float spaceFreq = 1200.0f, const unsigned int sps = 16, const float rrcAlpha = 0.5f, const unsigned int rrcSyms = 7);

      virtual void set_alpha(const float alpha) = 0;
    };

  } // namespace amateur
} // namespace gr

#endif /* INCLUDED_AMATEUR_BURST_AFSK_MODULATOR_H */

