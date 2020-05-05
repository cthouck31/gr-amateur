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

from gnuradio import gr
import pmt
from AX25_Utils import octetsToBits, nrzToNrzi

class AX25_Packet_Encoder(gr.basic_block):
    """
    docstring for block AX25_Packet_Encoder
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            "AX25_Packet_Encoder",
            in_sig=None, out_sig=None)

        # Message ports for data packets.
        self.message_port_register_in(pmt.intern("data"))
        self.message_port_register_out(pmt.intern("pkt"))

        self.set_msg_handler(pmt.intern("data"), self._handleInput)

    def _handleInput(self, msg):
        # Check message type.
        if not pmt.is_pair(msg):
            line = "Invalid input data type detected, must be a pair (car=pmt.NIL, cdr=pmt.init_u8vector([...]))."
            logger.error(line)
            print(line)
            return

        # Unpack data bytes.
        value = pmt.cdr(msg)
        if not pmt.is_u8vector(value):
            line = "Invalid value type, must be a u8vector (cdr=%s)." % str(value)
            logger.error(line)
            print(line)
            return
        octets = pmt.to_python(value)

        line = "Input: {}".format(",".join(["0x{:02x}".format(bi) for bi in octets]))
        logger.debug(line)

        # Encode
        bitSeq = octetsToBits(octets)

        # Forward message.
        self.message_port_pub(pmt.intern("pkt"), msg)
