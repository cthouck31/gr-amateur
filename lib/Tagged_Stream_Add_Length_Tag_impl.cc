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
#include "Tagged_Stream_Add_Length_Tag_impl.h"

namespace gr {
  namespace amateur {

    Tagged_Stream_Add_Length_Tag::sptr
    Tagged_Stream_Add_Length_Tag::make(const std::string &lengthTag, const int offset, const unsigned int typeSize)
    {
      return gnuradio::get_initial_sptr
        (new Tagged_Stream_Add_Length_Tag_impl(lengthTag, offset, typeSize));
    }

    /*
     * The private constructor
     */
    Tagged_Stream_Add_Length_Tag_impl::Tagged_Stream_Add_Length_Tag_impl(const std::string &lengthTag, const int offset, const unsigned int typeSize)
      : gr::sync_block("Tagged_Stream_Add_Length_Tag",
              gr::io_signature::make(1, 1, typeSize),
              gr::io_signature::make(1, 1, typeSize)),
        d_lengthTag(pmt::intern(lengthTag)),
        d_typeSize(typeSize),
        d_offset(offset)
    {
        // Must manually add tags back.
        set_tag_propagation_policy(TPP_DONT);
    }

    /*
     * Our virtual destructor.
     */
    Tagged_Stream_Add_Length_Tag_impl::~Tagged_Stream_Add_Length_Tag_impl()
    {}

    int
    Tagged_Stream_Add_Length_Tag_impl::work(int noutput_items,
        gr_vector_const_void_star &input_items,
        gr_vector_void_star &output_items)
    {
      int length = 0;
      unsigned int k;
      std::vector<tag_t> tags;
      const unsigned char *in = (const unsigned char *) input_items[0];
      unsigned char *out = (unsigned char*) output_items[0];

      // Modify all length tags.
      get_tags_in_range(tags,
                        0,
                        nitems_read(0),
                        nitems_read(0)+noutput_items,
                        d_lengthTag);

      for (k = 0; k < tags.size(); k++)
      {
          // Check for valid length.
          if (!pmt::is_integer(tags[k].value))
          {
              continue;
          }

          // Compute new length.
          length = (int) pmt::to_long(tags[k].value);
          length = length + d_offset;
          // Only add tags with valid lengths back to stream.
          if (length > 0)
          {
              tags[k].srcid = pmt::intern("tagged_stream_add_length_tag");
              tags[k].value = pmt::from_long((unsigned int)length);
              add_item_tag(0, tags[k]);
          }
      }

      // Copy all items over.
      memcpy(out, in, d_typeSize*noutput_items);

      // Tell runtime system how many output items we produced.
      return noutput_items;
    }

  } /* namespace amateur */
} /* namespace gr */

