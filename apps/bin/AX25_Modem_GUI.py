#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AX.25 - AFSK1200 Modem GUI
# Author: cthouck31
# Description: GUI for the AX.25 - AFSK1200 Modem application.
# Generated: Thu May  7 01:02:52 2020
##################################################

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt5 import Qt
from PyQt5 import Qt, QtCore
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import qtgui
from gnuradio import zeromq
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import ConfigParser
import amateur
import logging; logging.basicConfig()
import sip
import sys
from gnuradio import qtgui


class AX25_Modem_GUI(gr.top_block, Qt.QWidget):

    def __init__(self, configFile="~/.config/gr-amateur/AX25_Modem-HackRF-RTLSDR.ini", logLevel="debug"):
        gr.top_block.__init__(self, "AX.25 - AFSK1200 Modem GUI")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AX.25 - AFSK1200 Modem GUI")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "AX25_Modem_GUI")

        if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
            self.restoreGeometry(self.settings.value("geometry").toByteArray())
        else:
            self.restoreGeometry(self.settings.value("geometry", type=QtCore.QByteArray))

        ##################################################
        # Parameters
        ##################################################
        self.configFile = configFile
        self.logLevel = logLevel

        ##################################################
        # Variables
        ##################################################
        self._rx_fs_config = ConfigParser.ConfigParser()
        self._rx_fs_config.read(configFile)
        try: rx_fs = self._rx_fs_config.getfloat('Receive', 'fs')
        except: rx_fs = 1.92e6
        self.rx_fs = rx_fs
        self.logLvl = logLvl = {"info": logging.INFO, "debug": logging.DEBUG, "warning": logging.WARNING, "warn": logging.WARN, "error": logging.ERROR}.get(logLevel.lower(), logging.INFO)
        self._afsk_bitRate_config = ConfigParser.ConfigParser()
        self._afsk_bitRate_config.read(configFile)
        try: afsk_bitRate = self._afsk_bitRate_config.getfloat('AFSK', 'bitRate')
        except: afsk_bitRate = 1200.0
        self.afsk_bitRate = afsk_bitRate
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0 = ""
        self.variable_qtgui_label_0 = variable_qtgui_label_0 = ""
        self._rx_freq_config = ConfigParser.ConfigParser()
        self._rx_freq_config.read(configFile)
        try: rx_freq = self._rx_freq_config.getfloat('Receive', 'freq')
        except: rx_freq = 93.1e6
        self.rx_freq = rx_freq
        self._rx_deviceArgs_config = ConfigParser.ConfigParser()
        self._rx_deviceArgs_config.read(configFile)
        try: rx_deviceArgs = self._rx_deviceArgs_config.get('Receive', 'deviceArgs')
        except: rx_deviceArgs = ""
        self.rx_deviceArgs = rx_deviceArgs
        self.rootLogger = rootLogger = amateur.setupLogging(level=logLvl)
        self._debug_txCtrl_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_txCtrl_zmqAddr_config.read(configFile)
        try: debug_txCtrl_zmqAddr = self._debug_txCtrl_zmqAddr_config.get('Debug', 'txCtrl_zmqAddr')
        except: debug_txCtrl_zmqAddr = "tcp://127.0.0.1:18737"
        self.debug_txCtrl_zmqAddr = debug_txCtrl_zmqAddr
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
        self._debug_rxCtrl_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_rxCtrl_zmqAddr_config.read(configFile)
        try: debug_rxCtrl_zmqAddr = self._debug_rxCtrl_zmqAddr_config.get('Debug', 'rxCtrl_zmqAddr')
        except: debug_rxCtrl_zmqAddr = "tcp://127.0.0.1:18738"
        self.debug_rxCtrl_zmqAddr = debug_rxCtrl_zmqAddr
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
        self.Fs_bb = Fs_bb = min([rx_fs/afsk_bitRate, 20]) * afsk_bitRate

        ##################################################
        # Blocks
        ##################################################
        self.statTab = Qt.QTabWidget()
        self.statTab_widget_0 = Qt.QWidget()
        self.statTab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.statTab_widget_0)
        self.statTab_grid_layout_0 = Qt.QGridLayout()
        self.statTab_layout_0.addLayout(self.statTab_grid_layout_0)
        self.statTab.addTab(self.statTab_widget_0, 'Statistics')
        self.top_grid_layout.addWidget(self.statTab, 0, 6, 3, 2)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,3)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(6,8)]
        self.plotTab = Qt.QTabWidget()
        self.plotTab_widget_0 = Qt.QWidget()
        self.plotTab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plotTab_widget_0)
        self.plotTab_grid_layout_0 = Qt.QGridLayout()
        self.plotTab_layout_0.addLayout(self.plotTab_grid_layout_0)
        self.plotTab.addTab(self.plotTab_widget_0, 'Spectrum')
        self.plotTab_widget_1 = Qt.QWidget()
        self.plotTab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.plotTab_widget_1)
        self.plotTab_grid_layout_1 = Qt.QGridLayout()
        self.plotTab_layout_1.addLayout(self.plotTab_grid_layout_1)
        self.plotTab.addTab(self.plotTab_widget_1, 'Time')
        self.top_grid_layout.addWidget(self.plotTab, 0, 0, 8, 6)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(0,8)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,6)]
        self.msgTab = Qt.QTabWidget()
        self.msgTab_widget_0 = Qt.QWidget()
        self.msgTab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.msgTab_widget_0)
        self.msgTab_grid_layout_0 = Qt.QGridLayout()
        self.msgTab_layout_0.addLayout(self.msgTab_grid_layout_0)
        self.msgTab.addTab(self.msgTab_widget_0, 'Messages')
        self.msgTab_widget_1 = Qt.QWidget()
        self.msgTab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.msgTab_widget_1)
        self.msgTab_grid_layout_1 = Qt.QGridLayout()
        self.msgTab_layout_1.addLayout(self.msgTab_grid_layout_1)
        self.msgTab.addTab(self.msgTab_widget_1, 'Console')
        self.msgTab_widget_2 = Qt.QWidget()
        self.msgTab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.msgTab_widget_2)
        self.msgTab_grid_layout_2 = Qt.QGridLayout()
        self.msgTab_layout_2.addLayout(self.msgTab_grid_layout_2)
        self.msgTab.addTab(self.msgTab_widget_2, 'Beacon')
        self.top_grid_layout.addWidget(self.msgTab, 8, 0, 8, 8)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(8,16)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(0,8)]
        self.ctrlTab = Qt.QTabWidget()
        self.ctrlTab_widget_0 = Qt.QWidget()
        self.ctrlTab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.ctrlTab_widget_0)
        self.ctrlTab_grid_layout_0 = Qt.QGridLayout()
        self.ctrlTab_layout_0.addLayout(self.ctrlTab_grid_layout_0)
        self.ctrlTab.addTab(self.ctrlTab_widget_0, 'Control')
        self.top_grid_layout.addWidget(self.ctrlTab, 3, 6, 5, 2)
        [self.top_grid_layout.setRowStretch(r,1) for r in range(3,8)]
        [self.top_grid_layout.setColumnStretch(c,1) for c in range(6,8)]
        self.zeromq_sub_source_0_0_0_0 = zeromq.sub_source(gr.sizeof_char, 1, debug_cs_zmqAddr, 5, False, -1)
        self.zeromq_sub_source_0_0_0 = zeromq.sub_source(gr.sizeof_float, 1, debug_syms_zmqAddr, 10, False, -1)
        self.zeromq_sub_source_0_0 = zeromq.sub_source(gr.sizeof_float, 1, debug_snr_zmqAddr, 10, False, -1)
        self.zeromq_sub_source_0 = zeromq.sub_source(gr.sizeof_gr_complex, 1, debug_bb_zmqAddr, 10, False, -1)
        self.zeromq_sub_msg_source_0_0_0 = zeromq.sub_msg_source(debug_stats_zmqAddr, 10)
        self.zeromq_sub_msg_source_0_0 = zeromq.sub_msg_source(debug_sent_zmqAddr, 10)
        self.zeromq_sub_msg_source_0 = zeromq.sub_msg_source(debug_recv_zmqAddr, 10)
        self.zeromq_pub_msg_sink_0_0_0_0 = zeromq.pub_msg_sink(debug_rxCtrl_zmqAddr, 10)
        self.zeromq_pub_msg_sink_0_0_0 = zeromq.pub_msg_sink(debug_txCtrl_zmqAddr, 10)
        self._variable_qtgui_label_0_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_0_formatter = None
        else:
          self._variable_qtgui_label_0_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_0_tool_bar.addWidget(Qt.QLabel("Transmit"+": "))
        self._variable_qtgui_label_0_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_0_formatter(self.variable_qtgui_label_0_0)))
        self._variable_qtgui_label_0_0_tool_bar.addWidget(self._variable_qtgui_label_0_0_label)
        self.msgTab_grid_layout_0.addWidget(self._variable_qtgui_label_0_0_tool_bar, 0, 0, 1, 4)
        [self.msgTab_grid_layout_0.setRowStretch(r,1) for r in range(0,1)]
        [self.msgTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,4)]
        self._variable_qtgui_label_0_tool_bar = Qt.QToolBar(self)

        if None:
          self._variable_qtgui_label_0_formatter = None
        else:
          self._variable_qtgui_label_0_formatter = lambda x: str(x)

        self._variable_qtgui_label_0_tool_bar.addWidget(Qt.QLabel("Receive"+": "))
        self._variable_qtgui_label_0_label = Qt.QLabel(str(self._variable_qtgui_label_0_formatter(self.variable_qtgui_label_0)))
        self._variable_qtgui_label_0_tool_bar.addWidget(self._variable_qtgui_label_0_label)
        self.msgTab_grid_layout_0.addWidget(self._variable_qtgui_label_0_tool_bar, 0, 4, 1, 4)
        [self.msgTab_grid_layout_0.setRowStretch(r,1) for r in range(0,1)]
        [self.msgTab_grid_layout_0.setColumnStretch(c,1) for c in range(4,8)]
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rx_freq, #fc
        	Fs_bb, #bw
        	"", #name
                1 #number of inputs
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.025)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)

        if not False:
          self.qtgui_waterfall_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_waterfall_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-100, 0)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.plotTab_grid_layout_0.addWidget(self._qtgui_waterfall_sink_x_0_win, 3, 0, 5, 8)
        [self.plotTab_grid_layout_0.setRowStretch(r,1) for r in range(3,8)]
        [self.plotTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,8)]
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_f(
        	int(afsk_bitRate * 2), #size
        	afsk_bitRate, #samp_rate
        	"Symbols", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-1.25, 1.25)

        self.qtgui_time_sink_x_0_0.set_y_label("", "")

        self.qtgui_time_sink_x_0_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.plotTab_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_0_win, 4, 0, 4, 8)
        [self.plotTab_grid_layout_1.setRowStretch(r,1) for r in range(4,8)]
        [self.plotTab_grid_layout_1.setColumnStretch(c,1) for c in range(0,8)]
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	int(Fs_bb * 2), #size
        	Fs_bb, #samp_rate
        	"SNR", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-10, 30)

        self.qtgui_time_sink_x_0.set_y_label("", "")

        self.qtgui_time_sink_x_0.enable_tags(-1, True)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_axis_labels(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        self.qtgui_time_sink_x_0.enable_stem_plot(False)

        if not True:
          self.qtgui_time_sink_x_0.disable_legend()

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.plotTab_grid_layout_1.addWidget(self._qtgui_time_sink_x_0_win, 0, 0, 4, 8)
        [self.plotTab_grid_layout_1.setRowStretch(r,1) for r in range(0,4)]
        [self.plotTab_grid_layout_1.setColumnStretch(c,1) for c in range(0,8)]
        self.qtgui_number_sink_0_0 = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            2
        )
        self.qtgui_number_sink_0_0.set_update_time(0.10)
        self.qtgui_number_sink_0_0.set_title("")

        labels = ["{:8s}".format("SNR"), "{:8s}".format("CS"), '', '', '',
                  '', '', '', '', '']
        units = ["dB", '', '', '', '',
                 '', '', '', '', '']
        colors = [("blue", "red"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
                  ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        for i in xrange(2):
            self.qtgui_number_sink_0_0.set_min(i, -5)
            self.qtgui_number_sink_0_0.set_max(i, 20)
            self.qtgui_number_sink_0_0.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.qtgui_number_sink_0_0.set_label(i, "Data {0}".format(i))
            else:
                self.qtgui_number_sink_0_0.set_label(i, labels[i])
            self.qtgui_number_sink_0_0.set_unit(i, units[i])
            self.qtgui_number_sink_0_0.set_factor(i, factor[i])

        self.qtgui_number_sink_0_0.enable_autoscale(False)
        self._qtgui_number_sink_0_0_win = sip.wrapinstance(self.qtgui_number_sink_0_0.pyqwidget(), Qt.QWidget)
        self.statTab_grid_layout_0.addWidget(self._qtgui_number_sink_0_0_win, 0, 0, 1, 4)
        [self.statTab_grid_layout_0.setRowStretch(r,1) for r in range(0,1)]
        [self.statTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,4)]
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
        	4096, #size
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	rx_freq, #fc
        	Fs_bb, #bw
        	"Spectrum", #name
        	1 #number of inputs
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.1)
        self.qtgui_freq_sink_x_0.set_y_axis(-100, 0)
        self.qtgui_freq_sink_x_0.set_y_label("", "dB")
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)

        if not False:
          self.qtgui_freq_sink_x_0.disable_legend()

        if "complex" == "float" or "complex" == "msg_float":
          self.qtgui_freq_sink_x_0.set_plot_pos_half(not True)

        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["green", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.pyqwidget(), Qt.QWidget)
        self.plotTab_grid_layout_0.addWidget(self._qtgui_freq_sink_x_0_win, 0, 0, 3, 8)
        [self.plotTab_grid_layout_0.setRowStretch(r,1) for r in range(0,3)]
        [self.plotTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,8)]
        self.qtgui_edit_box_msg_0_1 = qtgui.edit_box_msg(qtgui.FLOAT, '', "TX - Gain", True, True, "gain")
        self._qtgui_edit_box_msg_0_1_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_1.pyqwidget(), Qt.QWidget)
        self.ctrlTab_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_1_win, 2, 0, 1, 1)
        [self.ctrlTab_grid_layout_0.setRowStretch(r,1) for r in range(2,3)]
        [self.ctrlTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,1)]
        self.qtgui_edit_box_msg_0_0_0 = qtgui.edit_box_msg(qtgui.FLOAT, '', "RX - Gain", True, True, "gain")
        self._qtgui_edit_box_msg_0_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0_0.pyqwidget(), Qt.QWidget)
        self.ctrlTab_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_0_0_win, 3, 0, 1, 1)
        [self.ctrlTab_grid_layout_0.setRowStretch(r,1) for r in range(3,4)]
        [self.ctrlTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,1)]
        self.qtgui_edit_box_msg_0_0 = qtgui.edit_box_msg(qtgui.FLOAT, '', "RX - Frequency", True, True, "freq")
        self._qtgui_edit_box_msg_0_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0_0.pyqwidget(), Qt.QWidget)
        self.ctrlTab_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_0_win, 1, 0, 1, 1)
        [self.ctrlTab_grid_layout_0.setRowStretch(r,1) for r in range(1,2)]
        [self.ctrlTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,1)]
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.FLOAT, '', "TX - Frequency", True, True, "freq")
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.pyqwidget(), Qt.QWidget)
        self.ctrlTab_grid_layout_0.addWidget(self._qtgui_edit_box_msg_0_win, 0, 0, 1, 1)
        [self.ctrlTab_grid_layout_0.setRowStretch(r,1) for r in range(0,1)]
        [self.ctrlTab_grid_layout_0.setColumnStretch(c,1) for c in range(0,1)]
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.amateur_AX25_Packet_Decoder_0_0 = amateur.AX25_Packet_Decoder()
        self.amateur_AX25_Packet_Decoder_0 = amateur.AX25_Packet_Decoder()

        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.zeromq_pub_msg_sink_0_0_0, 'in'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.qtgui_freq_sink_x_0, 'freq'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.qtgui_waterfall_sink_x_0, 'freq'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0, 'msg'), (self.zeromq_pub_msg_sink_0_0_0_0, 'in'))
        self.msg_connect((self.qtgui_edit_box_msg_0_0_0, 'msg'), (self.zeromq_pub_msg_sink_0_0_0_0, 'in'))
        self.msg_connect((self.qtgui_edit_box_msg_0_1, 'msg'), (self.zeromq_pub_msg_sink_0_0_0, 'in'))
        self.msg_connect((self.zeromq_sub_msg_source_0, 'out'), (self.amateur_AX25_Packet_Decoder_0, 'in'))
        self.msg_connect((self.zeromq_sub_msg_source_0_0, 'out'), (self.amateur_AX25_Packet_Decoder_0_0, 'in'))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.qtgui_number_sink_0_0, 1))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0_0, 0), (self.qtgui_number_sink_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0, 0), (self.qtgui_time_sink_x_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0, 0), (self.qtgui_time_sink_x_0_0, 0))
        self.connect((self.zeromq_sub_source_0_0_0_0, 0), (self.blocks_uchar_to_float_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AX25_Modem_GUI")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_configFile(self):
        return self.configFile

    def set_configFile(self, configFile):
        self.configFile = configFile
        self._rx_freq_config = ConfigParser.ConfigParser()
        self._rx_freq_config.read(self.configFile)
        if not self._rx_freq_config.has_section('Receive'):
        	self._rx_freq_config.add_section('Receive')
        self._rx_freq_config.set('Receive', 'freq', str(None))
        self._rx_freq_config.write(open(self.configFile, 'w'))
        self._debug_txCtrl_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_txCtrl_zmqAddr_config.read(self.configFile)
        if not self._debug_txCtrl_zmqAddr_config.has_section('Debug'):
        	self._debug_txCtrl_zmqAddr_config.add_section('Debug')
        self._debug_txCtrl_zmqAddr_config.set('Debug', 'txCtrl_zmqAddr', str(None))
        self._debug_txCtrl_zmqAddr_config.write(open(self.configFile, 'w'))
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
        self._debug_rxCtrl_zmqAddr_config = ConfigParser.ConfigParser()
        self._debug_rxCtrl_zmqAddr_config.read(self.configFile)
        if not self._debug_rxCtrl_zmqAddr_config.has_section('Debug'):
        	self._debug_rxCtrl_zmqAddr_config.add_section('Debug')
        self._debug_rxCtrl_zmqAddr_config.set('Debug', 'rxCtrl_zmqAddr', str(None))
        self._debug_rxCtrl_zmqAddr_config.write(open(self.configFile, 'w'))
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
        self._afsk_bitRate_config = ConfigParser.ConfigParser()
        self._afsk_bitRate_config.read(self.configFile)
        if not self._afsk_bitRate_config.has_section('AFSK'):
        	self._afsk_bitRate_config.add_section('AFSK')
        self._afsk_bitRate_config.set('AFSK', 'bitRate', str(None))
        self._afsk_bitRate_config.write(open(self.configFile, 'w'))
        self._rx_fs_config = ConfigParser.ConfigParser()
        self._rx_fs_config.read(self.configFile)
        if not self._rx_fs_config.has_section('Receive'):
        	self._rx_fs_config.add_section('Receive')
        self._rx_fs_config.set('Receive', 'fs', str(None))
        self._rx_fs_config.write(open(self.configFile, 'w'))
        self._rx_deviceArgs_config = ConfigParser.ConfigParser()
        self._rx_deviceArgs_config.read(self.configFile)
        if not self._rx_deviceArgs_config.has_section('Receive'):
        	self._rx_deviceArgs_config.add_section('Receive')
        self._rx_deviceArgs_config.set('Receive', 'deviceArgs', str(None))
        self._rx_deviceArgs_config.write(open(self.configFile, 'w'))

    def get_logLevel(self):
        return self.logLevel

    def set_logLevel(self, logLevel):
        self.logLevel = logLevel

    def get_rx_fs(self):
        return self.rx_fs

    def set_rx_fs(self, rx_fs):
        self.rx_fs = rx_fs
        self.set_Fs_bb(min([self.rx_fs/self.afsk_bitRate, 20]) * self.afsk_bitRate)

    def get_logLvl(self):
        return self.logLvl

    def set_logLvl(self, logLvl):
        self.logLvl = logLvl
        self.set_rootLogger(amateur.setupLogging(level=self.logLvl))

    def get_afsk_bitRate(self):
        return self.afsk_bitRate

    def set_afsk_bitRate(self, afsk_bitRate):
        self.afsk_bitRate = afsk_bitRate
        self.set_Fs_bb(min([self.rx_fs/self.afsk_bitRate, 20]) * self.afsk_bitRate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.afsk_bitRate)

    def get_variable_qtgui_label_0_0(self):
        return self.variable_qtgui_label_0_0

    def set_variable_qtgui_label_0_0(self, variable_qtgui_label_0_0):
        self.variable_qtgui_label_0_0 = variable_qtgui_label_0_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0_0))

    def get_variable_qtgui_label_0(self):
        return self.variable_qtgui_label_0

    def set_variable_qtgui_label_0(self, variable_qtgui_label_0):
        self.variable_qtgui_label_0 = variable_qtgui_label_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_label_0_label, "setText", Qt.Q_ARG("QString", self.variable_qtgui_label_0))

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.Fs_bb)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq, self.Fs_bb)

    def get_rx_deviceArgs(self):
        return self.rx_deviceArgs

    def set_rx_deviceArgs(self, rx_deviceArgs):
        self.rx_deviceArgs = rx_deviceArgs

    def get_rootLogger(self):
        return self.rootLogger

    def set_rootLogger(self, rootLogger):
        self.rootLogger = rootLogger

    def get_debug_txCtrl_zmqAddr(self):
        return self.debug_txCtrl_zmqAddr

    def set_debug_txCtrl_zmqAddr(self, debug_txCtrl_zmqAddr):
        self.debug_txCtrl_zmqAddr = debug_txCtrl_zmqAddr

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

    def get_debug_rxCtrl_zmqAddr(self):
        return self.debug_rxCtrl_zmqAddr

    def set_debug_rxCtrl_zmqAddr(self, debug_rxCtrl_zmqAddr):
        self.debug_rxCtrl_zmqAddr = debug_rxCtrl_zmqAddr

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

    def get_Fs_bb(self):
        return self.Fs_bb

    def set_Fs_bb(self, Fs_bb):
        self.Fs_bb = Fs_bb
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.rx_freq, self.Fs_bb)
        self.qtgui_time_sink_x_0.set_samp_rate(self.Fs_bb)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.rx_freq, self.Fs_bb)


def argument_parser():
    description = 'GUI for the AX.25 - AFSK1200 Modem application.'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--configFile", dest="configFile", type="string", default="~/.config/gr-amateur/AX25_Modem-HackRF-RTLSDR.ini",
        help="Set Configuration File [default=%default]")
    parser.add_option(
        "", "--logLevel", dest="logLevel", type="string", default="debug",
        help="Set Log Level [default=%default]")
    return parser


def main(top_block_cls=AX25_Modem_GUI, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls(configFile=options.configFile, logLevel=options.logLevel)
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.aboutToQuit.connect(quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
