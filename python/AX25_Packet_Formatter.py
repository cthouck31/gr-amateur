# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AX.25 Packet Formatter
# Generated: Sat Apr 18 15:27:06 2020
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import amateur


class AX25_Packet_Formatter(gr.hier_block2):

    def __init__(self, frameTag="packet_len", numRevs=20):
        gr.hier_block2.__init__(
            self, "AX.25 Packet Formatter",
            gr.io_signature(0, 0, 0),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_in("in")
        self.message_port_register_hier_out("out")

        ##################################################
        # Parameters
        ##################################################
        self.frameTag = frameTag
        self.numRevs = numRevs

        ##################################################
        # Blocks
        ##################################################
        self.digital_hdlc_framer_pb_0 = digital.hdlc_framer_pb(frameTag)
        self.blocks_vector_source_x_0 = blocks.vector_source_b(tuple([0,1,1,1,1,1,1,0] * numRevs), True, 1, [])
        self.blocks_tagged_stream_to_pdu_0 = blocks.tagged_stream_to_pdu(blocks.byte_t, frameTag)
        self.blocks_tagged_stream_mux_0 = blocks.tagged_stream_mux(gr.sizeof_char*1, frameTag, 0)
        self.blocks_stream_to_tagged_stream_0 = blocks.stream_to_tagged_stream(gr.sizeof_char, 1, numRevs * 8, frameTag)
        self.amateur_Tagged_Nrzi_Encoder_0 = amateur.Tagged_Nrzi_Encoder(frameTag, 1)
        self.amateur_AX25_Packet_Encoder_0 = amateur.AX25_Packet_Encoder()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.amateur_AX25_Packet_Encoder_0, 'pkt'), (self.digital_hdlc_framer_pb_0, 'in'))
        self.msg_connect((self.blocks_tagged_stream_to_pdu_0, 'pdus'), (self, 'out'))
        self.msg_connect((self, 'in'), (self.amateur_AX25_Packet_Encoder_0, 'data'))
        self.connect((self.amateur_Tagged_Nrzi_Encoder_0, 0), (self.blocks_tagged_stream_to_pdu_0, 0))
        self.connect((self.blocks_stream_to_tagged_stream_0, 0), (self.blocks_tagged_stream_mux_0, 0))
        self.connect((self.blocks_tagged_stream_mux_0, 0), (self.amateur_Tagged_Nrzi_Encoder_0, 0))
        self.connect((self.blocks_vector_source_x_0, 0), (self.blocks_stream_to_tagged_stream_0, 0))
        self.connect((self.digital_hdlc_framer_pb_0, 0), (self.blocks_tagged_stream_mux_0, 1))

    def get_frameTag(self):
        return self.frameTag

    def set_frameTag(self, frameTag):
        self.frameTag = frameTag

    def get_numRevs(self):
        return self.numRevs

    def set_numRevs(self, numRevs):
        self.numRevs = numRevs
        self.blocks_vector_source_x_0.set_data(tuple([0,1,1,1,1,1,1,0] * self.numRevs), [])
        self.blocks_stream_to_tagged_stream_0.set_packet_len(self.numRevs * 8)
        self.blocks_stream_to_tagged_stream_0.set_packet_len_pmt(self.numRevs * 8)
