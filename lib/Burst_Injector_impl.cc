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
#include "Burst_Injector_impl.h"

namespace gr {
  namespace amateur {

    Burst_Injector::sptr
    Burst_Injector::make(const std::string &lengthTag)
    {
      return gnuradio::get_initial_sptr
        (new Burst_Injector_impl(lengthTag));
    }

    /*
     * The private constructor
     */
    Burst_Injector_impl::Burst_Injector_impl(const std::string &lengthTag)
      : gr::sync_block("Burst_Injector",
              gr::io_signature::make(0, 0, 0),
              gr::io_signature::make(1, 1, sizeof(gr_complex))),
      d_frameTag(pmt::intern(lengthTag)),
      d_newBurst(0)
    {
        message_port_register_in(pmt::intern("in"));
        set_msg_handler(pmt::intern("in"),
                        boost::bind(&Burst_Injector_impl::_handleMessage,
                                    this, _1));
    }

    /*
     * Our virtual destructor.
     */
    Burst_Injector_impl::~Burst_Injector_impl()
    {
    }

    void
    Burst_Injector_impl::_handleMessage(pmt::pmt_t &msg)
    {
      std::vector<gr_complex> data;
      // Check message type.
      pmt::pmt_t value = pmt::cdr(msg);
      if (!pmt::is_c32vector(value))
      {
          std::cerr << "Invalid input type." << std::endl;
          return;
      }

      // Get samples.
      data = pmt::c32vector_elements(value);
      if (data.empty())
      {
          return;
      }

      // Add samples to transmit queue.
      gr::thread::scoped_lock lock(d_lock);
      d_newBurst = 1;
      d_burst.insert(d_burst.begin(),
                     data.begin(),
                     data.begin() + data.size());
    };

    int
    Burst_Injector_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      tag_t tag;
      unsigned int numSent = 0;
      gr_complex *out = (gr_complex *) output_items[0];

      // Lock work function.
      gr::thread::scoped_lock lock(d_lock);
      numSent = std::min((unsigned int)noutput_items,
                         (unsigned int)d_burst.size());
      // Send any data.
      if (numSent > 0)
      {
          if (d_newBurst)
          {
              tag.offset = nitems_written(0);
              tag.srcid  = pmt::intern("burst_injector");
              tag.key    = d_frameTag;
              tag.value  = pmt::from_long(d_burst.size());
              add_item_tag(0, tag);

              d_newBurst = 0;
          }
          memcpy(out, &d_burst[0], sizeof(gr_complex)*numSent);
          d_burst.erase(d_burst.begin(), d_burst.begin()+numSent);
      }
      // Pad w/ zeros.
      memset(out+numSent, 0, sizeof(gr_complex)*(noutput_items - numSent));

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace amateur */
} /* namespace gr */

