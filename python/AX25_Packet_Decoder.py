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

import json
import numpy
from gnuradio import gr
import pmt
from AX25_Utils import Ax25_bytesToPacket

class AX25_Packet_Decoder(gr.basic_block):
    """
    docstring for block AX25_Packet_Decoder
    """
    def __init__(self):
        gr.basic_block.__init__(self,
            name="AX25_Packet_Decoder",
            in_sig=None,
            out_sig=None)

        self.message_port_register_in(pmt.intern("in"))
        self.message_port_register_out(pmt.intern("out"))
        self.message_port_register_out(pmt.intern("dict"))
        self.message_port_register_out(pmt.intern("str"))
        self.set_msg_handler(pmt.intern("in"), self.handler)

        self.recvCnt = 0

    def handler(self, msg):
        value = pmt.cdr(msg)
        if not pmt.is_u8vector(value):
            return

        octets = pmt.to_python(value)

        packet = {}
        try:
            packet = Ax25_bytesToPacket(octets)
            line = "".join([chr(ci) for ci in packet.get("info", [])])
            self.recvCnt += 1
        except Exception as e:
            print("Error parsing AX.25: %s" % str(e))
            return

        # Create JSON string.
        pktStr = str(packet)
        pktMsg = pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol(pktStr))

        # Create pretty string.
        src   = packet.get("src",  "None")
        dst   = packet.get("dest", "None")
        reps  = packet.get("repeaters", [])
        ctrl  = packet.get("ctrl", {})
        ptype = ctrl.get("type", "")
        proto = packet.get("proto", 0)
        info  = "".join([chr(ci) for ci in packet.get("info", [])])

        repStr = ""
        for rep in reps:
            repStr += "{}{} (ssid={})\n".format(" "*13,
                                              str(rep.get("callsign", "None")),
                                              rep.get("ssid", -1))

        # String format.
        pktPretty = ("------------------------------\n"
                     "Source:      {} (ssid={})\n"
                     "Destination: {} (ssid={})\n"
                     "Type:        {} (proto={})\n"
                     "Repeaters:\n"
                     "{}"
                     "Info:\n"
                     "{}\n").format(str(src.get("callsign", "None")), src.get("ssid", -1),
                                    str(dst.get("callsign", "None")), dst.get("ssid", -1),
                                    ptype, proto,
                                    repStr,
                                    info)
        pktPrettyMsg = pmt.cons(pmt.PMT_NIL, pmt.string_to_symbol(pktPretty))
        print(pktStr)

        self.message_port_pub(pmt.intern("out"), msg)
        self.message_port_pub(pmt.intern("dict"), pktMsg)
        self.message_port_pub(pmt.intern("str"), pktPrettyMsg)

    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        pass
