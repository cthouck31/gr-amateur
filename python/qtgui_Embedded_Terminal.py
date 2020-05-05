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

from PyQt5 import (Qt, QtCore, QtGui, QtWidgets)

import shlex
import subprocess
import numpy
from gnuradio import gr


class qtgui_Embedded_Terminal(gr.basic_block, QtWidgets.QWidget):
    """
    Simple embedded terminal emulator.

    Usage:
        User enters a terminal command in the 'prompt' line at the bottom of the widget and presses return to execute it.
        The command is then executed and the resulting output is printed in the text box.
        Note: This component is a very basic terminal utility. Executing complex commands or modifying filesystems is strongly discouraged.

    Args:
        blacklist (list)    : List of executable commands to prevent (default=['exit', 'reboot', 'poweroff', 'rm -rf /', 'rm -rf /home']).

    Returns:
        A QT GUI block for GNU Radio that performs terminal emulation.
    """
    def __init__(self, blacklist=["exit", "reboot", "poweroff", "rm -rf /", "rm -rf /home"], *args, **kwargs):
        gr.basic_block.__init__(self,
            name="qtgui_Embedded_Terminal",
            in_sig=None,
            out_sig=None)

        QtWidgets.QWidget.__init__(self, *args, **kwargs)

        self.blacklist = blacklist
        self.prompt    = "$> "

        self.lineLbl  = QtWidgets.QLabel(self.prompt)
        self.lineLbl.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit = QtWidgets.QLineEdit()
        self.textBox  = QtWidgets.QTextEdit()
        self.textBox.ensureCursorVisible()
        self.textBox.setReadOnly(True)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.textBox,  0, 0, 4, 16)
        layout.addWidget(self.lineLbl,  4, 0, 1, 1)
        layout.addWidget(self.lineEdit, 4, 1, 1, 15)
        self.setLayout(layout)

        self.connect(self.lineEdit,
                     Qt.SIGNAL("returnPressed(void)"),
                     self.runCmd)

    def runCmd(self):
        cmd   = str(self.lineEdit.text())
        cmd   = cmd.lstrip(self.prompt)
        argStr = " ".join(cmd.strip().split())
        args = shlex.split(argStr)

        # Skip empty lines.
        if len(args) == 0:
            self.textBox.append(" ")
            self.lineEdit.clear()
            return

        for c in self.blacklist:
            if args[0].lower().find(c.lower()) >= 0:
                logger.error("\'%s\' command in black list, skipping execution..." %
                             args[0])
                self.textBox.append(" ")
                self.lineEdit.clear()
                return

        try:
            self.textBox.append("$> " + cmd)
            logger.debug("%s" % str(args))
            proc  = subprocess.Popen(args,
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            if len(stdout) > 0:
                self.textBox.append(stdout)
            if len(stderr) > 0:
                self.textBox.append(stderr)
        except Exception as e:
            logger.error("Failed to run command \'%s\': %s." % (cmd, str(e)))

        self.lineEdit.clear()



    def forecast(self, noutput_items, ninput_items_required):
        #setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        pass
