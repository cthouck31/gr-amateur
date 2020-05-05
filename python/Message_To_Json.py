#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#
import logging
logger = logging.getLogger(__name__)

import pmt
from gnuradio import gr


class Message_To_Json(gr.sync_block):
    """
    docstring for block Message_To_Json
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="Message_To_Json",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern("pdus"))
        self.message_port_register_out(pmt.intern("json"))
        self.set_msg_handler(pmt.intern("pdus"), self._handler)

    def _handler(self, msg):
        try:
            item = pmt.to_python(msg)
        except Exception as e:
            logger.error("Failed to parse PMT: %s." % str(e))
            return

        print(item)
        print(dict(item))

    def work(self, input_items, output_items):
        pass

