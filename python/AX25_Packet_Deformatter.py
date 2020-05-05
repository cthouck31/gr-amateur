# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AX.25 Packet Deformatter
# Generated: Sat Apr 18 19:56:31 2020
##################################################

from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
import amateur


class AX25_Packet_Deformatter(gr.hier_block2):

    def __init__(self):
        gr.hier_block2.__init__(
            self, "AX.25 Packet Deformatter",
            gr.io_signature(1, 1, gr.sizeof_char*1),
            gr.io_signature(0, 0, 0),
        )
        self.message_port_register_hier_out("out")

        ##################################################
        # Blocks
        ##################################################
        self.digital_hdlc_deframer_bp_0 = digital.hdlc_deframer_bp(8, 512)
        self.digital_diff_decoder_bb_0 = digital.diff_decoder_bb(2)
        self.blocks_not_xx_0 = blocks.not_bb()
        self.blocks_and_const_xx_0 = blocks.and_const_bb(0x01)
        self.amateur_AX25_Packet_Decoder_0 = amateur.AX25_Packet_Decoder()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.amateur_AX25_Packet_Decoder_0, 'out'), (self, 'out'))
        self.msg_connect((self.digital_hdlc_deframer_bp_0, 'out'), (self.amateur_AX25_Packet_Decoder_0, 'in'))
        self.connect((self.blocks_and_const_xx_0, 0), (self.digital_hdlc_deframer_bp_0, 0))
        self.connect((self.blocks_not_xx_0, 0), (self.blocks_and_const_xx_0, 0))
        self.connect((self.digital_diff_decoder_bb_0, 0), (self.blocks_not_xx_0, 0))
        self.connect((self, 0), (self.digital_diff_decoder_bb_0, 0))
