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

from PyQt5 import (Qt, QtGui, QtCore, QtWidgets)

import numpy
import pmt
from gnuradio import gr

class qtgui_Terminal_Sink(gr.sync_block, QtWidgets.QTextEdit):
    """
    QT GUI block to print incoming PDUs to a text box.

    Args:
        fontSize (int)              : Desired font size (not implemented).
        label (str)                 : Label for sink (not implemented).
        append (bool)               : Append input to the text box, otherwise flush it every write [default=True].
        logbook (logging.Logger)    : Optional logger object to write input messages to [default=<module logger>].

    Returns:
        QT GUI block for message output in GNU Radio.
    """
    __pyqtSignals__ = ("updateText(QString)")
    def __init__(self, fontSize=10, label="", append=True, *args, **kwargs):
        gr.sync_block.__init__(self, "qtgui_Terminal_Sink",[],[])

        QtWidgets.QTextEdit.__init__(self, *args, **kwargs)
        self.message_port_register_in(pmt.intern("pdus"))
        self.set_msg_handler(pmt.intern("pdus"), self._msgHandler)
        if append:
            QtCore.QObject.connect(self,
                                   QtCore.SIGNAL("updateText(QString)"),
                                   self,
                                   QtCore.SLOT("append(QString)"))
        else:
            QtCore.QObject.connect(self,
                                   QtCore.SIGNAL("updateText(QString)"),
                                   self,
                                   QtCore.SLOT("setText(QString)"))
        self.setReadOnly(True)
        self.show()

        # Optional logging object.
        self.logBook  = kwargs.get("logbook", logger)

    def _msgHandler(self, msg):
        if not pmt.is_pair(msg):
            logger.error("Invalid input message (expected PMT pair).")
            return

        # Convert to Python format.
        data = pmt.cdr(msg)
        try:
            item = pmt.to_python(data)
            if not isinstance(item, str):
                item = item.tostring()
        except Exception as e:
            logger.error("Failed to convert PMT to Python: %s." % str(e))
            return

        # Write item to log.
        self.logBook.debug(item)

        # Send to update slot.
        self.emit(QtCore.SIGNAL("updateText(QString)"), item)

    def work(self, input_items, output_items):
        pass
