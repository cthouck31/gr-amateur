#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AX.25 - AFSK1200 Modem
# Author: cthouck31
# Description: Modem for communicating via AX.25 w/ AFSK1200 modulation (APRS, etc).
# Generated: Wed Apr 29 00:14:55 2020
##################################################

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from AX25_AFSK1200_Modulator import AX25_AFSK1200_Modulator  # grc-generated hier_block
from AX25_AFSK_Demodulator import AX25_AFSK_Demodulator  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import amateur
import logging; logging.basicConfig()
import math
import osmosdr
import pmt
import time


class AX25_Modem(gr.top_block):

    def __init__(self, configFile="~/.config/gr-amateur/AX25_Modem-HackRF-RTLSDR.ini", logLevel="debug"):
        gr.top_block.__init__(self, "AX.25 - AFSK1200 Modem")

        ##################################################
        # Parameters
        ##################################################
        self.configFile = configFile
        self.logLevel = logLevel

        ##################################################
        # Variables
        ##################################################
        self.settings_0 = settings_0 = pmt.make_dict()
        self._rx_freq_config = ConfigParser.ConfigParser()
        self._rx_freq_config.read(configFile)
        try: rx_freq = self._rx_freq_config.getfloat('Receive', 'freq')
        except: rx_freq = 144.390e6
        self.rx_freq = rx_freq
        self.settings_1 = settings_1 = pmt.dict_add(settings_0, pmt.intern("rx_freq"), pmt.from_float(rx_freq))
        self.logLvl = logLvl = {"info": logging.INFO, "debug": logging.DEBUG, "warning": logging.WARNING, "warn": logging.WARN, "error": logging.ERROR}.get(logLevel.lower(), logging.INFO)
        self._tx_rfGain_config = ConfigParser.ConfigParser()
        self._tx_rfGain_config.read(configFile)
        try: tx_rfGain = self._tx_rfGain_config.getfloat('Transmit', 'rfGain')
        except: tx_rfGain = 0
        self.tx_rfGain = tx_rfGain
        self._tx_ppm_config = ConfigParser.ConfigParser()
        self._tx_ppm_config.read(configFile)
        try: tx_ppm = self._tx_ppm_config.getfloat('Transmit', 'ppm')
        except: tx_ppm = 26
        self.tx_ppm = tx_ppm
        self._tx_ifGain_config = ConfigParser.ConfigParser()
        self._tx_ifGain_config.read(configFile)
        try: tx_ifGain = self._tx_ifGain_config.getfloat('Transmit', 'ifGain')
        except: tx_ifGain = 10.0
        self.tx_ifGain = tx_ifGain
        self._tx_fs_config = ConfigParser.ConfigParser()
        self._tx_fs_config.read(configFile)
        try: tx_fs = self._tx_fs_config.getfloat('Transmit', 'fs')
        except: tx_fs = 8e6
        self.tx_fs = tx_fs
        self._tx_freq_config = ConfigParser.ConfigParser()
        self._tx_freq_config.read(configFile)
        try: tx_freq = self._tx_freq_config.getfloat('Transmit', 'freq')
        except: tx_freq = 144.390e6
        self.tx_freq = tx_freq
        self._tx_deviceArgs_config = ConfigParser.ConfigParser()
        self._tx_deviceArgs_config.read(configFile)
        try: tx_deviceArgs = self._tx_deviceArgs_config.get('Transmit', 'deviceArgs')
        except: tx_deviceArgs = ""
        self.tx_deviceArgs = tx_deviceArgs
        self._tx_bw_config = ConfigParser.ConfigParser()
        self._tx_bw_config.read(configFile)
        try: tx_bw = self._tx_bw_config.getfloat('Transmit', 'bw')
        except: tx_bw = 0.1e6
        self.tx_bw = tx_bw
        self._tx_bbGain_config = ConfigParser.ConfigParser()
        self._tx_bbGain_config.read(configFile)
        try: tx_bbGain = self._tx_bbGain_config.getfloat('Transmit', 'bbGain')
        except: tx_bbGain = 0
        self.tx_bbGain = tx_bbGain
        self._tx_ant_config = ConfigParser.ConfigParser()
        self._tx_ant_config.read(configFile)
        try: tx_ant = self._tx_ant_config.get('Transmit', 'ant')
        except: tx_ant = "TX/RX"
        self.tx_ant = tx_ant
        self.settings = settings = settings_1
        self._rx_rfGain_config = ConfigParser.ConfigParser()
        self._rx_rfGain_config.read(configFile)
        try: rx_rfGain = self._rx_rfGain_config.getfloat('Receive', 'rfGain')
        except: rx_rfGain = 45.0
        self.rx_rfGain = rx_rfGain
        self._rx_ppm_config = ConfigParser.ConfigParser()
        self._rx_ppm_config.read(configFile)
        try: rx_ppm = self._rx_ppm_config.getfloat('Receive', 'ppm')
        except: rx_ppm = 51
        self.rx_ppm = rx_ppm
        self._rx_ifGain_config = ConfigParser.ConfigParser()
        self._rx_ifGain_config.read(configFile)
        try: rx_ifGain = self._rx_ifGain_config.getfloat('Receive', 'ifGain')
        except: rx_ifGain = 0
        self.rx_ifGain = rx_ifGain
        self._rx_fs_config = ConfigParser.ConfigParser()
        self._rx_fs_config.read(configFile)
        try: rx_fs = self._rx_fs_config.getfloat('Receive', 'fs')
        except: rx_fs = 1.92e6
        self.rx_fs = rx_fs
        self._rx_deviceArgs_config = ConfigParser.ConfigParser()
        self._rx_deviceArgs_config.read(configFile)
        try: rx_deviceArgs = self._rx_deviceArgs_config.get('Receive', 'deviceArgs')
        except: rx_deviceArgs = ""
        self.rx_deviceArgs = rx_deviceArgs
        self._rx_bw_config = ConfigParser.ConfigParser()
        self._rx_bw_config.read('/home/cth/workspace/ham/gr-amateur/config/aprs-tx_hackrf-rx_rtlsdr.conf')
        try: rx_bw = self._rx_bw_config.getfloat('[Receive]', 'bw')
        except: rx_bw = 0.1e6
        self.rx_bw = rx_bw
        self._rx_bbGain_config = ConfigParser.ConfigParser()
        self._rx_bbGain_config.read(configFile)
        try: rx_bbGain = self._rx_bbGain_config.getfloat('Receive', 'bbGain')
        except: rx_bbGain = 0
        self.rx_bbGain = rx_bbGain
        self._rx_ant_config = ConfigParser.ConfigParser()
        self._rx_ant_config.read(configFile)
        try: rx_ant = self._rx_ant_config.get('Receive', 'ant')
        except: rx_ant = "RX"
        self.rx_ant = rx_ant
        self.rootLogger = rootLogger = amateur.setupLogging(level=logLvl)
        self._demod_pllLoopBw_config = ConfigParser.ConfigParser()
        self._demod_pllLoopBw_config.read(configFile)
        try: demod_pllLoopBw = self._demod_pllLoopBw_config.getfloat('Demod', 'pllLoopBw')
        except: demod_pllLoopBw = 2.0*3.1415926 / 350.0
        self.demod_pllLoopBw = demod_pllLoopBw
        self._demod_pllFreqMax_config = ConfigParser.ConfigParser()
        self._demod_pllFreqMax_config.read(configFile)
        try: demod_pllFreqMax = self._demod_pllFreqMax_config.getfloat('Demod', 'pllFreqMax')
        except: demod_pllFreqMax = 2.0*3.1415926 / 20.0
        self.demod_pllFreqMax = demod_pllFreqMax
        self._demod_agcEnable_config = ConfigParser.ConfigParser()
        self._demod_agcEnable_config.read(configFile)
        try: demod_agcEnable = self._demod_agcEnable_config.getint('Demod', 'agcEnable')
        except: demod_agcEnable = 1
        self.demod_agcEnable = demod_agcEnable
        self._demod_agcDecay_config = ConfigParser.ConfigParser()
        self._demod_agcDecay_config.read(configFile)
        try: demod_agcDecay = self._demod_agcDecay_config.getfloat('Demod', 'agcAttack')
        except: demod_agcDecay = 0.01
        self.demod_agcDecay = demod_agcDecay
        self._demod_agcAttack_config = ConfigParser.ConfigParser()
        self._demod_agcAttack_config.read(configFile)
        try: demod_agcAttack = self._demod_agcAttack_config.getfloat('Demod', 'agcAttack')
        except: demod_agcAttack = 0.1
        self.demod_agcAttack = demod_agcAttack
        self._debug_syms_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_syms_zmqAddr_config.read(configFile)
        try: debug_syms_zmqAddr = self._debug_syms_zmqAddr_config.get('Debug', 'syms_zmqAddr')
        except: debug_syms_zmqAddr = "tcp://127.0.0.1:18732"
        self.debug_syms_zmqAddr = debug_syms_zmqAddr
        self._debug_stats_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_stats_zmqAddr_config.read(configFile)
        try: debug_stats_zmqAddr = self._debug_stats_zmqAddr_config.get('Debug', 'stats_zmqAddr')
        except: debug_stats_zmqAddr = "tcp://127.0.0.1:18735"
        self.debug_stats_zmqAddr = debug_stats_zmqAddr
        self._debug_snr_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_snr_zmqAddr_config.read(configFile)
        try: debug_snr_zmqAddr = self._debug_snr_zmqAddr_config.get('Debug', 'snr_zmqAddr')
        except: debug_snr_zmqAddr = "tcp://127.0.0.1:18731"
        self.debug_snr_zmqAddr = debug_snr_zmqAddr
        self._debug_sent_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_sent_zmqAddr_config.read(configFile)
        try: debug_sent_zmqAddr = self._debug_sent_zmqAddr_config.get('Debug', 'sent_zmqAddr')
        except: debug_sent_zmqAddr = "tcp://127.0.0.1:18734"
        self.debug_sent_zmqAddr = debug_sent_zmqAddr
        self._debug_recv_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_recv_zmqAddr_config.read(configFile)
        try: debug_recv_zmqAddr = self._debug_recv_zmqAddr_config.get('Debug', 'recv_zmqAddr')
        except: debug_recv_zmqAddr = "tcp://127.0.0.1:18733"
        self.debug_recv_zmqAddr = debug_recv_zmqAddr
        self._debug_cs_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_cs_zmqAddr_config.read(configFile)
        try: debug_cs_zmqAddr = self._debug_cs_zmqAddr_config.get('Debug', 'cs_zmqAddr')
        except: debug_cs_zmqAddr = "tcp://127.0.0.1:18736"
        self.debug_cs_zmqAddr = debug_cs_zmqAddr
        self._debug_bb_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_bb_zmqAddr_config.read(configFile)
        try: debug_bb_zmqAddr = self._debug_bb_zmqAddr_config.get('Debug', 'bb_zmqAddr')
        except: debug_bb_zmqAddr = "tcp://127.0.0.1:18730"
        self.debug_bb_zmqAddr = debug_bb_zmqAddr
        self._csma_snrThreshold_config = ConfigParser.ConfigParser()
        self._csma_snrThreshold_config.read(configFile)
        try: csma_snrThreshold = self._csma_snrThreshold_config.getfloat('CSMA', 'snrThreshold')
        except: csma_snrThreshold = 2.0
        self.csma_snrThreshold = csma_snrThreshold
        self._csma_noiseAlpha_config = ConfigParser.ConfigParser()
        self._csma_noiseAlpha_config.read(configFile)
        try: csma_noiseAlpha = self._csma_noiseAlpha_config.getfloat('CSMA', 'noiseAlpha')
        except: csma_noiseAlpha = 0.00001
        self.csma_noiseAlpha = csma_noiseAlpha
        self._csma_enable_config = ConfigParser.ConfigParser()
        self._csma_enable_config.read(configFile)
        try: csma_enable = self._csma_enable_config.getint('CSMA', 'enable')
        except: csma_enable = 1
        self.csma_enable = csma_enable
        self._csma_avgAlpha_config = ConfigParser.ConfigParser()
        self._csma_avgAlpha_config.read(configFile)
        try: csma_avgAlpha = self._csma_avgAlpha_config.getfloat('CSMA', 'avgAlpha')
        except: csma_avgAlpha = 0.01
        self.csma_avgAlpha = csma_avgAlpha
        self._ax25_numPreambles_config = ConfigParser.ConfigParser()
        self._ax25_numPreambles_config.read(configFile)
        try: ax25_numPreambles = self._ax25_numPreambles_config.getint('AX25', 'numPreambles')
        except: ax25_numPreambles = 40
        self.ax25_numPreambles = ax25_numPreambles
        self._ax25_numPostambles_config = ConfigParser.ConfigParser()
        self._ax25_numPostambles_config.read(configFile)
        try: ax25_numPostambles = self._ax25_numPostambles_config.getint('AX25', 'numPostambles')
        except: ax25_numPostambles = 2
        self.ax25_numPostambles = ax25_numPostambles
        self._ax25_mtu_config = ConfigParser.ConfigParser()
        self._ax25_mtu_config.read(configFile)
        try: ax25_mtu = self._ax25_mtu_config.getint('AX25', 'mtu')
        except: ax25_mtu = 10000
        self.ax25_mtu = ax25_mtu
        self._ax25_ipPort_config = ConfigParser.ConfigParser()
        self._ax25_ipPort_config.read(configFile)
        try: ax25_ipPort = self._ax25_ipPort_config.get('AX25', 'ipPort')
        except: ax25_ipPort = '15331'
        self.ax25_ipPort = ax25_ipPort
        self._ax25_ipAddr_config = ConfigParser.ConfigParser()
        self._ax25_ipAddr_config.read(configFile)
        try: ax25_ipAddr = self._ax25_ipAddr_config.get('AX25', 'ipAddr')
        except: ax25_ipAddr = "127.0.0.1"
        self.ax25_ipAddr = ax25_ipAddr
        self._afsk_spaceFreq_config = ConfigParser.ConfigParser()
        self._afsk_spaceFreq_config.read(configFile)
        try: afsk_spaceFreq = self._afsk_spaceFreq_config.getfloat('AFSK', 'spaceFreq')
        except: afsk_spaceFreq = 2200.0
        self.afsk_spaceFreq = afsk_spaceFreq
        self._afsk_rolloff_config = ConfigParser.ConfigParser()
        self._afsk_rolloff_config.read(configFile)
        try: afsk_rolloff = self._afsk_rolloff_config.getfloat('AFSK', 'rolloff')
        except: afsk_rolloff = 0.7
        self.afsk_rolloff = afsk_rolloff
        self._afsk_markFreq_config = ConfigParser.ConfigParser()
        self._afsk_markFreq_config.read(configFile)
        try: afsk_markFreq = self._afsk_markFreq_config.getfloat('AFSK', 'markFreq')
        except: afsk_markFreq = 1200.0
        self.afsk_markFreq = afsk_markFreq
        self._afsk_frameTag_config = ConfigParser.ConfigParser()
        self._afsk_frameTag_config.read(configFile)
        try: afsk_frameTag = self._afsk_frameTag_config.get('AFSK', 'frameTag')
        except: afsk_frameTag = "tx_len"
        self.afsk_frameTag = afsk_frameTag
        self._afsk_filterSyms_config = ConfigParser.ConfigParser()
        self._afsk_filterSyms_config.read(configFile)
        try: afsk_filterSyms = self._afsk_filterSyms_config.getint('AFSK', 'filterSyms')
        except: afsk_filterSyms = 7
        self.afsk_filterSyms = afsk_filterSyms
        self._afsk_dcInsert_config = ConfigParser.ConfigParser()
        self._afsk_dcInsert_config.read(configFile)
        try: afsk_dcInsert = self._afsk_dcInsert_config.getint('AFSK', 'dcInsert')
        except: afsk_dcInsert = 1
        self.afsk_dcInsert = afsk_dcInsert
        self._afsk_bitRate_config = ConfigParser.ConfigParser()
        self._afsk_bitRate_config.read(configFile)
        try: afsk_bitRate = self._afsk_bitRate_config.getfloat('AFSK', 'bitRate')
        except: afsk_bitRate = 1200.0
        self.afsk_bitRate = afsk_bitRate

        ##################################################
        # Blocks
        ##################################################
        self.zeromq_pub_sink_0_0_0_0 = zeromq.pub_sink(gr.sizeof_char, 1, debug_cs_zmqAddr, 10, False, -1)
        self.zeromq_pub_sink_0_0_0 = zeromq.pub_sink(gr.sizeof_float, 1, debug_syms_zmqAddr, 10, False, -1)
        self.zeromq_pub_sink_0_0 = zeromq.pub_sink(gr.sizeof_float, 1, debug_snr_zmqAddr, 10, False, -1)
        self.zeromq_pub_sink_0 = zeromq.pub_sink(gr.sizeof_gr_complex, 1, debug_bb_zmqAddr, 10, False, -1)
        self.zeromq_pub_msg_sink_0_0_0 = zeromq.pub_msg_sink(debug_stats_zmqAddr, 10)
        self.zeromq_pub_msg_sink_0_0 = zeromq.pub_msg_sink(debug_sent_zmqAddr, 10)
        self.zeromq_pub_msg_sink_0 = zeromq.pub_msg_sink(debug_recv_zmqAddr, 10)
        self.single_pole_iir_filter_xx_0_0 = filter.single_pole_iir_filter_ff(csma_avgAlpha, 1)
        self.single_pole_iir_filter_xx_0 = filter.single_pole_iir_filter_ff(csma_noiseAlpha, 1)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + rx_deviceArgs )
        self.osmosdr_source_0.set_sample_rate(rx_fs)
        self.osmosdr_source_0.set_center_freq(rx_freq, 0)
        self.osmosdr_source_0.set_freq_corr(rx_ppm, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rx_rfGain, 0)
        self.osmosdr_source_0.set_if_gain(rx_ifGain, 0)
        self.osmosdr_source_0.set_bb_gain(rx_bbGain, 0)
        self.osmosdr_source_0.set_antenna(rx_ant, 0)
        self.osmosdr_source_0.set_bandwidth(rx_bw, 0)
          
        self.osmosdr_sink_0 = osmosdr.sink( args="numchan=" + str(1) + " " + tx_deviceArgs )
        self.osmosdr_sink_0.set_sample_rate(tx_fs)
        self.osmosdr_sink_0.set_center_freq(tx_freq, 0)
        self.osmosdr_sink_0.set_freq_corr(tx_ppm, 0)
        self.osmosdr_sink_0.set_gain(tx_rfGain, 0)
        self.osmosdr_sink_0.set_if_gain(tx_ifGain, 0)
        self.osmosdr_sink_0.set_bb_gain(tx_bbGain, 0)
        self.osmosdr_sink_0.set_antenna(tx_ant, 0)
        self.osmosdr_sink_0.set_bandwidth(tx_bw, 0)
          
        self.blocks_transcendental_0_0 = blocks.transcendental('log', "float")
        self.blocks_transcendental_0 = blocks.transcendental('log', "float")
        self.blocks_threshold_ff_0 = blocks.threshold_ff(csma_snrThreshold, csma_snrThreshold, 0)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_CLIENT", ax25_ipAddr, ax25_ipPort, ax25_mtu, False)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((20.0/math.log(10), ))
        self.blocks_message_strobe_0 = blocks.message_strobe(settings, 250)
        self.blocks_float_to_uchar_0 = blocks.float_to_uchar()
        self.blocks_complex_to_mag_0 = blocks.complex_to_mag(1)
        self.blocks_and_const_xx_0 = blocks.and_const_bb(0x01 if (csma_enable) else 0x00)
        self.analog_agc2_xx_0 = analog.agc2_cc(demod_agcAttack if (demod_agcEnable) else 0.0, demod_agcDecay if (demod_agcEnable) else 0.0, 1.0, 1.0)
        self.analog_agc2_xx_0.set_max_gain(65536)
        self.amateur_KISS_TNC_0 = amateur.KISS_TNC(afsk_bitRate, ax25_numPreambles, ax25_numPostambles, 0, 1)
        self.AX25_AFSK_Demodulator_0 = AX25_AFSK_Demodulator(
            Fs=rx_fs,
            Mark=afsk_markFreq,
            Rs=afsk_bitRate,
            Space=afsk_spaceFreq,
            alpha=afsk_rolloff,
            frameTag=afsk_frameTag,
            lockFreq=demod_pllFreqMax,
            loopBw=demod_pllLoopBw,
            numSyms=afsk_filterSyms,
        )
        self.AX25_AFSK1200_Modulator_0 = AX25_AFSK1200_Modulator(
            Fs=tx_fs,
            Mark=afsk_markFreq,
            Rs=afsk_bitRate,
            Space=afsk_spaceFreq,
            alpha=afsk_rolloff,
            dcInsert=afsk_dcInsert,
            frameTag=afsk_frameTag,
            numPost=ax25_numPostambles,
            numRevs=ax25_numPreambles,
            numSyms=afsk_filterSyms,
        )

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.AX25_AFSK_Demodulator_0, 'out'), (self.amateur_KISS_TNC_0, 'modem_resp'))    
        self.msg_connect((self.AX25_AFSK_Demodulator_0, 'out'), (self.zeromq_pub_msg_sink_0, 'in'))    
        self.msg_connect((self.amateur_KISS_TNC_0, 'modem_data'), (self.AX25_AFSK1200_Modulator_0, 'in'))    
        self.msg_connect((self.amateur_KISS_TNC_0, 'tnc_resp'), (self.blocks_socket_pdu_0, 'pdus'))    
        self.msg_connect((self.amateur_KISS_TNC_0, 'modem_data'), (self.zeromq_pub_msg_sink_0_0, 'in'))    
        self.msg_connect((self.blocks_message_strobe_0, 'strobe'), (self.zeromq_pub_msg_sink_0_0_0, 'in'))    
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.amateur_KISS_TNC_0, 'tnc_req'))    
        self.connect((self.AX25_AFSK1200_Modulator_0, 0), (self.osmosdr_sink_0, 0))    
        self.connect((self.AX25_AFSK_Demodulator_0, 2), (self.blocks_complex_to_mag_0, 0))    
        self.connect((self.AX25_AFSK_Demodulator_0, 2), (self.zeromq_pub_sink_0, 0))    
        self.connect((self.AX25_AFSK_Demodulator_0, 0), (self.zeromq_pub_sink_0_0_0, 0))    
        self.connect((self.analog_agc2_xx_0, 0), (self.AX25_AFSK_Demodulator_0, 0))    
        self.connect((self.blocks_and_const_xx_0, 0), (self.amateur_KISS_TNC_0, 0))    
        self.connect((self.blocks_and_const_xx_0, 0), (self.zeromq_pub_sink_0_0_0_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.single_pole_iir_filter_xx_0, 0))    
        self.connect((self.blocks_complex_to_mag_0, 0), (self.single_pole_iir_filter_xx_0_0, 0))    
        self.connect((self.blocks_float_to_uchar_0, 0), (self.blocks_and_const_xx_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_threshold_ff_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.zeromq_pub_sink_0_0, 0))    
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_uchar_0, 0))    
        self.connect((self.blocks_transcendental_0, 0), (self.blocks_sub_xx_0, 0))    
        self.connect((self.blocks_transcendental_0_0, 0), (self.blocks_sub_xx_0, 1))    
        self.connect((self.osmosdr_source_0, 0), (self.analog_agc2_xx_0, 0))    
        self.connect((self.single_pole_iir_filter_xx_0, 0), (self.blocks_transcendental_0_0, 0))    
        self.connect((self.single_pole_iir_filter_xx_0_0, 0), (self.blocks_transcendental_0, 0))    

    def get_configFile(self):
        return self.configFile

    def set_configFile(self, configFile):
        self.configFile = configFile
        self._tx_rfGain_config = ConfigParser.ConfigParser()
        self._tx_rfGain_config.read(self.configFile)
        if not self._tx_rfGain_config.has_section('Transmit'):
        	self._tx_rfGain_config.add_section('Transmit')
        self._tx_rfGain_config.set('Transmit', 'rfGain', str(None))
        self._tx_rfGain_config.write(open(self.configFile, 'w'))
        self._tx_ppm_config = ConfigParser.ConfigParser()
        self._tx_ppm_config.read(self.configFile)
        if not self._tx_ppm_config.has_section('Transmit'):
        	self._tx_ppm_config.add_section('Transmit')
        self._tx_ppm_config.set('Transmit', 'ppm', str(None))
        self._tx_ppm_config.write(open(self.configFile, 'w'))
        self._tx_ifGain_config = ConfigParser.ConfigParser()
        self._tx_ifGain_config.read(self.configFile)
        if not self._tx_ifGain_config.has_section('Transmit'):
        	self._tx_ifGain_config.add_section('Transmit')
        self._tx_ifGain_config.set('Transmit', 'ifGain', str(None))
        self._tx_ifGain_config.write(open(self.configFile, 'w'))
        self._tx_fs_config = ConfigParser.ConfigParser()
        self._tx_fs_config.read(self.configFile)
        if not self._tx_fs_config.has_section('Transmit'):
        	self._tx_fs_config.add_section('Transmit')
        self._tx_fs_config.set('Transmit', 'fs', str(None))
        self._tx_fs_config.write(open(self.configFile, 'w'))
        self._tx_freq_config = ConfigParser.ConfigParser()
        self._tx_freq_config.read(self.configFile)
        if not self._tx_freq_config.has_section('Transmit'):
        	self._tx_freq_config.add_section('Transmit')
        self._tx_freq_config.set('Transmit', 'freq', str(None))
        self._tx_freq_config.write(open(self.configFile, 'w'))
        self._tx_deviceArgs_config = ConfigParser.ConfigParser()
        self._tx_deviceArgs_config.read(self.configFile)
        if not self._tx_deviceArgs_config.has_section('Transmit'):
        	self._tx_deviceArgs_config.add_section('Transmit')
        self._tx_deviceArgs_config.set('Transmit', 'deviceArgs', str(None))
        self._tx_deviceArgs_config.write(open(self.configFile, 'w'))
        self._tx_bw_config = ConfigParser.ConfigParser()
        self._tx_bw_config.read(self.configFile)
        if not self._tx_bw_config.has_section('Transmit'):
        	self._tx_bw_config.add_section('Transmit')
        self._tx_bw_config.set('Transmit', 'bw', str(None))
        self._tx_bw_config.write(open(self.configFile, 'w'))
        self._tx_bbGain_config = ConfigParser.ConfigParser()
        self._tx_bbGain_config.read(self.configFile)
        if not self._tx_bbGain_config.has_section('Transmit'):
        	self._tx_bbGain_config.add_section('Transmit')
        self._tx_bbGain_config.set('Transmit', 'bbGain', str(None))
        self._tx_bbGain_config.write(open(self.configFile, 'w'))
        self._tx_ant_config = ConfigParser.ConfigParser()
        self._tx_ant_config.read(self.configFile)
        if not self._tx_ant_config.has_section('Transmit'):
        	self._tx_ant_config.add_section('Transmit')
        self._tx_ant_config.set('Transmit', 'ant', str(None))
        self._tx_ant_config.write(open(self.configFile, 'w'))
        self._rx_rfGain_config = ConfigParser.ConfigParser()
        self._rx_rfGain_config.read(self.configFile)
        if not self._rx_rfGain_config.has_section('Receive'):
        	self._rx_rfGain_config.add_section('Receive')
        self._rx_rfGain_config.set('Receive', 'rfGain', str(None))
        self._rx_rfGain_config.write(open(self.configFile, 'w'))
        self._rx_ppm_config = ConfigParser.ConfigParser()
        self._rx_ppm_config.read(self.configFile)
        if not self._rx_ppm_config.has_section('Receive'):
        	self._rx_ppm_config.add_section('Receive')
        self._rx_ppm_config.set('Receive', 'ppm', str(None))
        self._rx_ppm_config.write(open(self.configFile, 'w'))
        self._rx_ifGain_config = ConfigParser.ConfigParser()
        self._rx_ifGain_config.read(self.configFile)
        if not self._rx_ifGain_config.has_section('Receive'):
        	self._rx_ifGain_config.add_section('Receive')
        self._rx_ifGain_config.set('Receive', 'ifGain', str(None))
        self._rx_ifGain_config.write(open(self.configFile, 'w'))
        self._rx_fs_config = ConfigParser.ConfigParser()
        self._rx_fs_config.read(self.configFile)
        if not self._rx_fs_config.has_section('Receive'):
        	self._rx_fs_config.add_section('Receive')
        self._rx_fs_config.set('Receive', 'fs', str(None))
        self._rx_fs_config.write(open(self.configFile, 'w'))
        self._rx_freq_config = ConfigParser.ConfigParser()
        self._rx_freq_config.read(self.configFile)
        if not self._rx_freq_config.has_section('Receive'):
        	self._rx_freq_config.add_section('Receive')
        self._rx_freq_config.set('Receive', 'freq', str(None))
        self._rx_freq_config.write(open(self.configFile, 'w'))
        self._rx_deviceArgs_config = ConfigParser.ConfigParser()
        self._rx_deviceArgs_config.read(self.configFile)
        if not self._rx_deviceArgs_config.has_section('Receive'):
        	self._rx_deviceArgs_config.add_section('Receive')
        self._rx_deviceArgs_config.set('Receive', 'deviceArgs', str(None))
        self._rx_deviceArgs_config.write(open(self.configFile, 'w'))
        self._rx_bbGain_config = ConfigParser.ConfigParser()
        self._rx_bbGain_config.read(self.configFile)
        if not self._rx_bbGain_config.has_section('Receive'):
        	self._rx_bbGain_config.add_section('Receive')
        self._rx_bbGain_config.set('Receive', 'bbGain', str(None))
        self._rx_bbGain_config.write(open(self.configFile, 'w'))
        self._rx_ant_config = ConfigParser.ConfigParser()
        self._rx_ant_config.read(self.configFile)
        if not self._rx_ant_config.has_section('Receive'):
        	self._rx_ant_config.add_section('Receive')
        self._rx_ant_config.set('Receive', 'ant', str(None))
        self._rx_ant_config.write(open(self.configFile, 'w'))
        self._demod_pllLoopBw_config = ConfigParser.ConfigParser()
        self._demod_pllLoopBw_config.read(self.configFile)
        if not self._demod_pllLoopBw_config.has_section('Demod'):
        	self._demod_pllLoopBw_config.add_section('Demod')
        self._demod_pllLoopBw_config.set('Demod', 'pllLoopBw', str(None))
        self._demod_pllLoopBw_config.write(open(self.configFile, 'w'))
        self._demod_pllFreqMax_config = ConfigParser.ConfigParser()
        self._demod_pllFreqMax_config.read(self.configFile)
        if not self._demod_pllFreqMax_config.has_section('Demod'):
        	self._demod_pllFreqMax_config.add_section('Demod')
        self._demod_pllFreqMax_config.set('Demod', 'pllFreqMax', str(None))
        self._demod_pllFreqMax_config.write(open(self.configFile, 'w'))
        self._demod_agcEnable_config = ConfigParser.ConfigParser()
        self._demod_agcEnable_config.read(self.configFile)
        if not self._demod_agcEnable_config.has_section('Demod'):
        	self._demod_agcEnable_config.add_section('Demod')
        self._demod_agcEnable_config.set('Demod', 'agcEnable', str(None))
        self._demod_agcEnable_config.write(open(self.configFile, 'w'))
        self._demod_agcDecay_config = ConfigParser.ConfigParser()
        self._demod_agcDecay_config.read(self.configFile)
        if not self._demod_agcDecay_config.has_section('Demod'):
        	self._demod_agcDecay_config.add_section('Demod')
        self._demod_agcDecay_config.set('Demod', 'agcAttack', str(None))
        self._demod_agcDecay_config.write(open(self.configFile, 'w'))
        self._demod_agcAttack_config = ConfigParser.ConfigParser()
        self._demod_agcAttack_config.read(self.configFile)
        if not self._demod_agcAttack_config.has_section('Demod'):
        	self._demod_agcAttack_config.add_section('Demod')
        self._demod_agcAttack_config.set('Demod', 'agcAttack', str(None))
        self._demod_agcAttack_config.write(open(self.configFile, 'w'))
        self._debug_syms_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_syms_zmqAddr_config.read(self.configFile)
        if not self._debug_syms_zmqAddr_config.has_section('Debug'):
        	self._debug_syms_zmqAddr_config.add_section('Debug')
        self._debug_syms_zmqAddr_config.set('Debug', 'syms_zmqAddr', str(None))
        self._debug_syms_zmqAddr_config.write(open(self.configFile, 'w'))
        self._debug_stats_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_stats_zmqAddr_config.read(self.configFile)
        if not self._debug_stats_zmqAddr_config.has_section('Debug'):
        	self._debug_stats_zmqAddr_config.add_section('Debug')
        self._debug_stats_zmqAddr_config.set('Debug', 'stats_zmqAddr', str(None))
        self._debug_stats_zmqAddr_config.write(open(self.configFile, 'w'))
        self._debug_snr_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_snr_zmqAddr_config.read(self.configFile)
        if not self._debug_snr_zmqAddr_config.has_section('Debug'):
        	self._debug_snr_zmqAddr_config.add_section('Debug')
        self._debug_snr_zmqAddr_config.set('Debug', 'snr_zmqAddr', str(None))
        self._debug_snr_zmqAddr_config.write(open(self.configFile, 'w'))
        self._debug_sent_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_sent_zmqAddr_config.read(self.configFile)
        if not self._debug_sent_zmqAddr_config.has_section('Debug'):
        	self._debug_sent_zmqAddr_config.add_section('Debug')
        self._debug_sent_zmqAddr_config.set('Debug', 'sent_zmqAddr', str(None))
        self._debug_sent_zmqAddr_config.write(open(self.configFile, 'w'))
        self._debug_recv_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_recv_zmqAddr_config.read(self.configFile)
        if not self._debug_recv_zmqAddr_config.has_section('Debug'):
        	self._debug_recv_zmqAddr_config.add_section('Debug')
        self._debug_recv_zmqAddr_config.set('Debug', 'recv_zmqAddr', str(None))
        self._debug_recv_zmqAddr_config.write(open(self.configFile, 'w'))
        self._debug_cs_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_cs_zmqAddr_config.read(self.configFile)
        if not self._debug_cs_zmqAddr_config.has_section('Debug'):
        	self._debug_cs_zmqAddr_config.add_section('Debug')
        self._debug_cs_zmqAddr_config.set('Debug', 'cs_zmqAddr', str(None))
        self._debug_cs_zmqAddr_config.write(open(self.configFile, 'w'))
        self._debug_bb_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_bb_zmqAddr_config.read(self.configFile)
        if not self._debug_bb_zmqAddr_config.has_section('Debug'):
        	self._debug_bb_zmqAddr_config.add_section('Debug')
        self._debug_bb_zmqAddr_config.set('Debug', 'bb_zmqAddr', str(None))
        self._debug_bb_zmqAddr_config.write(open(self.configFile, 'w'))
        self._csma_snrThreshold_config = ConfigParser.ConfigParser()
        self._csma_snrThreshold_config.read(self.configFile)
        if not self._csma_snrThreshold_config.has_section('CSMA'):
        	self._csma_snrThreshold_config.add_section('CSMA')
        self._csma_snrThreshold_config.set('CSMA', 'snrThreshold', str(None))
        self._csma_snrThreshold_config.write(open(self.configFile, 'w'))
        self._csma_noiseAlpha_config = ConfigParser.ConfigParser()
        self._csma_noiseAlpha_config.read(self.configFile)
        if not self._csma_noiseAlpha_config.has_section('CSMA'):
        	self._csma_noiseAlpha_config.add_section('CSMA')
        self._csma_noiseAlpha_config.set('CSMA', 'noiseAlpha', str(None))
        self._csma_noiseAlpha_config.write(open(self.configFile, 'w'))
        self._csma_enable_config = ConfigParser.ConfigParser()
        self._csma_enable_config.read(self.configFile)
        if not self._csma_enable_config.has_section('CSMA'):
        	self._csma_enable_config.add_section('CSMA')
        self._csma_enable_config.set('CSMA', 'enable', str(None))
        self._csma_enable_config.write(open(self.configFile, 'w'))
        self._csma_avgAlpha_config = ConfigParser.ConfigParser()
        self._csma_avgAlpha_config.read(self.configFile)
        if not self._csma_avgAlpha_config.has_section('CSMA'):
        	self._csma_avgAlpha_config.add_section('CSMA')
        self._csma_avgAlpha_config.set('CSMA', 'avgAlpha', str(None))
        self._csma_avgAlpha_config.write(open(self.configFile, 'w'))
        self._ax25_numPreambles_config = ConfigParser.ConfigParser()
        self._ax25_numPreambles_config.read(self.configFile)
        if not self._ax25_numPreambles_config.has_section('AX25'):
        	self._ax25_numPreambles_config.add_section('AX25')
        self._ax25_numPreambles_config.set('AX25', 'numPreambles', str(None))
        self._ax25_numPreambles_config.write(open(self.configFile, 'w'))
        self._ax25_numPostambles_config = ConfigParser.ConfigParser()
        self._ax25_numPostambles_config.read(self.configFile)
        if not self._ax25_numPostambles_config.has_section('AX25'):
        	self._ax25_numPostambles_config.add_section('AX25')
        self._ax25_numPostambles_config.set('AX25', 'numPostambles', str(None))
        self._ax25_numPostambles_config.write(open(self.configFile, 'w'))
        self._ax25_mtu_config = ConfigParser.ConfigParser()
        self._ax25_mtu_config.read(self.configFile)
        if not self._ax25_mtu_config.has_section('AX25'):
        	self._ax25_mtu_config.add_section('AX25')
        self._ax25_mtu_config.set('AX25', 'mtu', str(None))
        self._ax25_mtu_config.write(open(self.configFile, 'w'))
        self._ax25_ipPort_config = ConfigParser.ConfigParser()
        self._ax25_ipPort_config.read(self.configFile)
        if not self._ax25_ipPort_config.has_section('AX25'):
        	self._ax25_ipPort_config.add_section('AX25')
        self._ax25_ipPort_config.set('AX25', 'ipPort', str(None))
        self._ax25_ipPort_config.write(open(self.configFile, 'w'))
        self._ax25_ipAddr_config = ConfigParser.ConfigParser()
        self._ax25_ipAddr_config.read(self.configFile)
        if not self._ax25_ipAddr_config.has_section('AX25'):
        	self._ax25_ipAddr_config.add_section('AX25')
        self._ax25_ipAddr_config.set('AX25', 'ipAddr', str(None))
        self._ax25_ipAddr_config.write(open(self.configFile, 'w'))
        self._afsk_spaceFreq_config = ConfigParser.ConfigParser()
        self._afsk_spaceFreq_config.read(self.configFile)
        if not self._afsk_spaceFreq_config.has_section('AFSK'):
        	self._afsk_spaceFreq_config.add_section('AFSK')
        self._afsk_spaceFreq_config.set('AFSK', 'spaceFreq', str(None))
        self._afsk_spaceFreq_config.write(open(self.configFile, 'w'))
        self._afsk_rolloff_config = ConfigParser.ConfigParser()
        self._afsk_rolloff_config.read(self.configFile)
        if not self._afsk_rolloff_config.has_section('AFSK'):
        	self._afsk_rolloff_config.add_section('AFSK')
        self._afsk_rolloff_config.set('AFSK', 'rolloff', str(None))
        self._afsk_rolloff_config.write(open(self.configFile, 'w'))
        self._afsk_markFreq_config = ConfigParser.ConfigParser()
        self._afsk_markFreq_config.read(self.configFile)
        if not self._afsk_markFreq_config.has_section('AFSK'):
        	self._afsk_markFreq_config.add_section('AFSK')
        self._afsk_markFreq_config.set('AFSK', 'markFreq', str(None))
        self._afsk_markFreq_config.write(open(self.configFile, 'w'))
        self._afsk_frameTag_config = ConfigParser.ConfigParser()
        self._afsk_frameTag_config.read(self.configFile)
        if not self._afsk_frameTag_config.has_section('AFSK'):
        	self._afsk_frameTag_config.add_section('AFSK')
        self._afsk_frameTag_config.set('AFSK', 'frameTag', str(None))
        self._afsk_frameTag_config.write(open(self.configFile, 'w'))
        self._afsk_filterSyms_config = ConfigParser.ConfigParser()
        self._afsk_filterSyms_config.read(self.configFile)
        if not self._afsk_filterSyms_config.has_section('AFSK'):
        	self._afsk_filterSyms_config.add_section('AFSK')
        self._afsk_filterSyms_config.set('AFSK', 'filterSyms', str(None))
        self._afsk_filterSyms_config.write(open(self.configFile, 'w'))
        self._afsk_dcInsert_config = ConfigParser.ConfigParser()
        self._afsk_dcInsert_config.read(self.configFile)
        if not self._afsk_dcInsert_config.has_section('AFSK'):
        	self._afsk_dcInsert_config.add_section('AFSK')
        self._afsk_dcInsert_config.set('AFSK', 'dcInsert', str(None))
        self._afsk_dcInsert_config.write(open(self.configFile, 'w'))
        self._afsk_bitRate_config = ConfigParser.ConfigParser()
        self._afsk_bitRate_config.read(self.configFile)
        if not self._afsk_bitRate_config.has_section('AFSK'):
        	self._afsk_bitRate_config.add_section('AFSK')
        self._afsk_bitRate_config.set('AFSK', 'bitRate', str(None))
        self._afsk_bitRate_config.write(open(self.configFile, 'w'))

    def get_logLevel(self):
        return self.logLevel

    def set_logLevel(self, logLevel):
        self.logLevel = logLevel

    def get_settings_0(self):
        return self.settings_0

    def set_settings_0(self, settings_0):
        self.settings_0 = settings_0
        self.set_settings_1(pmt.dict_add(self.settings_0, pmt.intern("rx_freq"), pmt.from_float(self.rx_freq)))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.set_settings_1(pmt.dict_add(self.settings_0, pmt.intern("rx_freq"), pmt.from_float(self.rx_freq)))
        self.osmosdr_source_0.set_center_freq(self.rx_freq, 0)

    def get_settings_1(self):
        return self.settings_1

    def set_settings_1(self, settings_1):
        self.settings_1 = settings_1
        self.set_settings(self.settings_1)

    def get_logLvl(self):
        return self.logLvl

    def set_logLvl(self, logLvl):
        self.logLvl = logLvl
        self.set_rootLogger(amateur.setupLogging(level=self.logLvl))

    def get_tx_rfGain(self):
        return self.tx_rfGain

    def set_tx_rfGain(self, tx_rfGain):
        self.tx_rfGain = tx_rfGain
        self.osmosdr_sink_0.set_gain(self.tx_rfGain, 0)

    def get_tx_ppm(self):
        return self.tx_ppm

    def set_tx_ppm(self, tx_ppm):
        self.tx_ppm = tx_ppm
        self.osmosdr_sink_0.set_freq_corr(self.tx_ppm, 0)

    def get_tx_ifGain(self):
        return self.tx_ifGain

    def set_tx_ifGain(self, tx_ifGain):
        self.tx_ifGain = tx_ifGain
        self.osmosdr_sink_0.set_if_gain(self.tx_ifGain, 0)

    def get_tx_fs(self):
        return self.tx_fs

    def set_tx_fs(self, tx_fs):
        self.tx_fs = tx_fs
        self.osmosdr_sink_0.set_sample_rate(self.tx_fs)
        self.AX25_AFSK1200_Modulator_0.set_Fs(self.tx_fs)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.osmosdr_sink_0.set_center_freq(self.tx_freq, 0)

    def get_tx_deviceArgs(self):
        return self.tx_deviceArgs

    def set_tx_deviceArgs(self, tx_deviceArgs):
        self.tx_deviceArgs = tx_deviceArgs

    def get_tx_bw(self):
        return self.tx_bw

    def set_tx_bw(self, tx_bw):
        self.tx_bw = tx_bw
        self.osmosdr_sink_0.set_bandwidth(self.tx_bw, 0)

    def get_tx_bbGain(self):
        return self.tx_bbGain

    def set_tx_bbGain(self, tx_bbGain):
        self.tx_bbGain = tx_bbGain
        self.osmosdr_sink_0.set_bb_gain(self.tx_bbGain, 0)

    def get_tx_ant(self):
        return self.tx_ant

    def set_tx_ant(self, tx_ant):
        self.tx_ant = tx_ant
        self.osmosdr_sink_0.set_antenna(self.tx_ant, 0)

    def get_settings(self):
        return self.settings

    def set_settings(self, settings):
        self.settings = settings
        self.blocks_message_strobe_0.set_msg(self.settings)

    def get_rx_rfGain(self):
        return self.rx_rfGain

    def set_rx_rfGain(self, rx_rfGain):
        self.rx_rfGain = rx_rfGain
        self.osmosdr_source_0.set_gain(self.rx_rfGain, 0)

    def get_rx_ppm(self):
        return self.rx_ppm

    def set_rx_ppm(self, rx_ppm):
        self.rx_ppm = rx_ppm
        self.osmosdr_source_0.set_freq_corr(self.rx_ppm, 0)

    def get_rx_ifGain(self):
        return self.rx_ifGain

    def set_rx_ifGain(self, rx_ifGain):
        self.rx_ifGain = rx_ifGain
        self.osmosdr_source_0.set_if_gain(self.rx_ifGain, 0)

    def get_rx_fs(self):
        return self.rx_fs

    def set_rx_fs(self, rx_fs):
        self.rx_fs = rx_fs
        self.osmosdr_source_0.set_sample_rate(self.rx_fs)
        self.AX25_AFSK_Demodulator_0.set_Fs(self.rx_fs)

    def get_rx_deviceArgs(self):
        return self.rx_deviceArgs

    def set_rx_deviceArgs(self, rx_deviceArgs):
        self.rx_deviceArgs = rx_deviceArgs

    def get_rx_bw(self):
        return self.rx_bw

    def set_rx_bw(self, rx_bw):
        self.rx_bw = rx_bw
        self.osmosdr_source_0.set_bandwidth(self.rx_bw, 0)

    def get_rx_bbGain(self):
        return self.rx_bbGain

    def set_rx_bbGain(self, rx_bbGain):
        self.rx_bbGain = rx_bbGain
        self.osmosdr_source_0.set_bb_gain(self.rx_bbGain, 0)

    def get_rx_ant(self):
        return self.rx_ant

    def set_rx_ant(self, rx_ant):
        self.rx_ant = rx_ant
        self.osmosdr_source_0.set_antenna(self.rx_ant, 0)

    def get_rootLogger(self):
        return self.rootLogger

    def set_rootLogger(self, rootLogger):
        self.rootLogger = rootLogger

    def get_demod_pllLoopBw(self):
        return self.demod_pllLoopBw

    def set_demod_pllLoopBw(self, demod_pllLoopBw):
        self.demod_pllLoopBw = demod_pllLoopBw
        self.AX25_AFSK_Demodulator_0.set_loopBw(self.demod_pllLoopBw)

    def get_demod_pllFreqMax(self):
        return self.demod_pllFreqMax

    def set_demod_pllFreqMax(self, demod_pllFreqMax):
        self.demod_pllFreqMax = demod_pllFreqMax
        self.AX25_AFSK_Demodulator_0.set_lockFreq(self.demod_pllFreqMax)

    def get_demod_agcEnable(self):
        return self.demod_agcEnable

    def set_demod_agcEnable(self, demod_agcEnable):
        self.demod_agcEnable = demod_agcEnable
        self.analog_agc2_xx_0.set_attack_rate(self.demod_agcAttack if (self.demod_agcEnable) else 0.0)
        self.analog_agc2_xx_0.set_decay_rate(self.demod_agcDecay if (self.demod_agcEnable) else 0.0)

    def get_demod_agcDecay(self):
        return self.demod_agcDecay

    def set_demod_agcDecay(self, demod_agcDecay):
        self.demod_agcDecay = demod_agcDecay
        self.analog_agc2_xx_0.set_decay_rate(self.demod_agcDecay if (self.demod_agcEnable) else 0.0)

    def get_demod_agcAttack(self):
        return self.demod_agcAttack

    def set_demod_agcAttack(self, demod_agcAttack):
        self.demod_agcAttack = demod_agcAttack
        self.analog_agc2_xx_0.set_attack_rate(self.demod_agcAttack if (self.demod_agcEnable) else 0.0)

    def get_debug_syms_zmqAddr(self):
        return self.debug_syms_zmqAddr

    def set_debug_syms_zmqAddr(self, debug_syms_zmqAddr):
        self.debug_syms_zmqAddr = debug_syms_zmqAddr

    def get_debug_stats_zmqAddr(self):
        return self.debug_stats_zmqAddr

    def set_debug_stats_zmqAddr(self, debug_stats_zmqAddr):
        self.debug_stats_zmqAddr = debug_stats_zmqAddr

    def get_debug_snr_zmqAddr(self):
        return self.debug_snr_zmqAddr

    def set_debug_snr_zmqAddr(self, debug_snr_zmqAddr):
        self.debug_snr_zmqAddr = debug_snr_zmqAddr

    def get_debug_sent_zmqAddr(self):
        return self.debug_sent_zmqAddr

    def set_debug_sent_zmqAddr(self, debug_sent_zmqAddr):
        self.debug_sent_zmqAddr = debug_sent_zmqAddr

    def get_debug_recv_zmqAddr(self):
        return self.debug_recv_zmqAddr

    def set_debug_recv_zmqAddr(self, debug_recv_zmqAddr):
        self.debug_recv_zmqAddr = debug_recv_zmqAddr

    def get_debug_cs_zmqAddr(self):
        return self.debug_cs_zmqAddr

    def set_debug_cs_zmqAddr(self, debug_cs_zmqAddr):
        self.debug_cs_zmqAddr = debug_cs_zmqAddr

    def get_debug_bb_zmqAddr(self):
        return self.debug_bb_zmqAddr

    def set_debug_bb_zmqAddr(self, debug_bb_zmqAddr):
        self.debug_bb_zmqAddr = debug_bb_zmqAddr

    def get_csma_snrThreshold(self):
        return self.csma_snrThreshold

    def set_csma_snrThreshold(self, csma_snrThreshold):
        self.csma_snrThreshold = csma_snrThreshold
        self.blocks_threshold_ff_0.set_hi(self.csma_snrThreshold)
        self.blocks_threshold_ff_0.set_lo(self.csma_snrThreshold)

    def get_csma_noiseAlpha(self):
        return self.csma_noiseAlpha

    def set_csma_noiseAlpha(self, csma_noiseAlpha):
        self.csma_noiseAlpha = csma_noiseAlpha
        self.single_pole_iir_filter_xx_0.set_taps(self.csma_noiseAlpha)

    def get_csma_enable(self):
        return self.csma_enable

    def set_csma_enable(self, csma_enable):
        self.csma_enable = csma_enable
        self.blocks_and_const_xx_0.set_k(0x01 if (self.csma_enable) else 0x00)

    def get_csma_avgAlpha(self):
        return self.csma_avgAlpha

    def set_csma_avgAlpha(self, csma_avgAlpha):
        self.csma_avgAlpha = csma_avgAlpha
        self.single_pole_iir_filter_xx_0_0.set_taps(self.csma_avgAlpha)

    def get_ax25_numPreambles(self):
        return self.ax25_numPreambles

    def set_ax25_numPreambles(self, ax25_numPreambles):
        self.ax25_numPreambles = ax25_numPreambles
        self.AX25_AFSK1200_Modulator_0.set_numRevs(self.ax25_numPreambles)

    def get_ax25_numPostambles(self):
        return self.ax25_numPostambles

    def set_ax25_numPostambles(self, ax25_numPostambles):
        self.ax25_numPostambles = ax25_numPostambles
        self.AX25_AFSK1200_Modulator_0.set_numPost(self.ax25_numPostambles)

    def get_ax25_mtu(self):
        return self.ax25_mtu

    def set_ax25_mtu(self, ax25_mtu):
        self.ax25_mtu = ax25_mtu

    def get_ax25_ipPort(self):
        return self.ax25_ipPort

    def set_ax25_ipPort(self, ax25_ipPort):
        self.ax25_ipPort = ax25_ipPort

    def get_ax25_ipAddr(self):
        return self.ax25_ipAddr

    def set_ax25_ipAddr(self, ax25_ipAddr):
        self.ax25_ipAddr = ax25_ipAddr

    def get_afsk_spaceFreq(self):
        return self.afsk_spaceFreq

    def set_afsk_spaceFreq(self, afsk_spaceFreq):
        self.afsk_spaceFreq = afsk_spaceFreq
        self.AX25_AFSK_Demodulator_0.set_Space(self.afsk_spaceFreq)
        self.AX25_AFSK1200_Modulator_0.set_Space(self.afsk_spaceFreq)

    def get_afsk_rolloff(self):
        return self.afsk_rolloff

    def set_afsk_rolloff(self, afsk_rolloff):
        self.afsk_rolloff = afsk_rolloff
        self.AX25_AFSK_Demodulator_0.set_alpha(self.afsk_rolloff)
        self.AX25_AFSK1200_Modulator_0.set_alpha(self.afsk_rolloff)

    def get_afsk_markFreq(self):
        return self.afsk_markFreq

    def set_afsk_markFreq(self, afsk_markFreq):
        self.afsk_markFreq = afsk_markFreq
        self.AX25_AFSK_Demodulator_0.set_Mark(self.afsk_markFreq)
        self.AX25_AFSK1200_Modulator_0.set_Mark(self.afsk_markFreq)

    def get_afsk_frameTag(self):
        return self.afsk_frameTag

    def set_afsk_frameTag(self, afsk_frameTag):
        self.afsk_frameTag = afsk_frameTag
        self.AX25_AFSK_Demodulator_0.set_frameTag(self.afsk_frameTag)
        self.AX25_AFSK1200_Modulator_0.set_frameTag(self.afsk_frameTag)

    def get_afsk_filterSyms(self):
        return self.afsk_filterSyms

    def set_afsk_filterSyms(self, afsk_filterSyms):
        self.afsk_filterSyms = afsk_filterSyms
        self.AX25_AFSK_Demodulator_0.set_numSyms(self.afsk_filterSyms)
        self.AX25_AFSK1200_Modulator_0.set_numSyms(self.afsk_filterSyms)

    def get_afsk_dcInsert(self):
        return self.afsk_dcInsert

    def set_afsk_dcInsert(self, afsk_dcInsert):
        self.afsk_dcInsert = afsk_dcInsert
        self.AX25_AFSK1200_Modulator_0.set_dcInsert(self.afsk_dcInsert)

    def get_afsk_bitRate(self):
        return self.afsk_bitRate

    def set_afsk_bitRate(self, afsk_bitRate):
        self.afsk_bitRate = afsk_bitRate
        self.AX25_AFSK_Demodulator_0.set_Rs(self.afsk_bitRate)
        self.AX25_AFSK1200_Modulator_0.set_Rs(self.afsk_bitRate)


def argument_parser():
    description = 'Modem for communicating via AX.25 w/ AFSK1200 modulation (APRS, etc).'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--configFile", dest="configFile", type="string", default="~/.config/gr-amateur/AX25_Modem-HackRF-RTLSDR.ini",
        help="Set Configuration File [default=%default]")
    parser.add_option(
        "", "--logLevel", dest="logLevel", type="string", default="debug",
        help="Set Log Level [default=%default]")
    return parser


def main(top_block_cls=AX25_Modem, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable real-time scheduling."

    tb = top_block_cls(configFile=options.configFile, logLevel=options.logLevel)
    tb.start()
    tb.wait()


if __name__ == '__main__':
    main()
