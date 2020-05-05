#
# Copyright 2008,2009 Free Software Foundation, Inc.
#
# This application is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This application is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

# The presence of this file turns this directory into a Python package

'''
This is the GNU Radio AMATEUR module. Place your Python package
description here (python/__init__.py).
'''

# import swig generated symbols into the amateur namespace
try:
	# this might fail if the module is python-only
	from amateur_swig import *
except ImportError:
	pass

# import any pure python here
from AX25_Packet_Encoder import AX25_Packet_Encoder
from AX25_Packet_Decoder import AX25_Packet_Decoder
from AX25_Packet_Formatter import AX25_Packet_Formatter
from AX25_Packet_Deformatter import AX25_Packet_Deformatter
from KISS_TNC import KISS_TNC
from qtgui_Terminal_Sink import qtgui_Terminal_Sink
from qtgui_Embedded_Terminal import qtgui_Embedded_Terminal
from Message_To_Json import Message_To_Json




import os
import logging

FILE_LOGGER_PATH   = os.path.join(os.path.expanduser("~"),
                          os.path.basename(os.path.dirname(__file__)))
FILE_LOGGER_FORMAT = "%(asctime)s [%(name)-12s][%(levelname)-8s]: %(message)s"
CONSOLE_LOGGER_FORMAT = "[%(name)-12s][%(levelname)-8s]: %(message)s"


def setupLogging(level=logging.INFO, path=FILE_LOGGER_PATH, disable=[]):
    """
    Setup logging configuration.

    Args:
        level:  Log level to set (from 'logging').
        path:   Path to output log file ('None' for no file log).

    Returns:
        Root logger object.
    """
    # Base logger.
    rootLogger = logging.getLogger()
    # Set level.
    rootLogger.setLevel(level)
    rootLogger.handlers = []
    if len(rootLogger.handlers):
        return rootLogger

    # Create file logger.
    if path != None:
        fileHandler = logging.FileHandler(path)
        fileFmt = logging.Formatter(FILE_LOGGER_FORMAT)
        fileHandler.setFormatter(fileFmt)
        rootLogger.addHandler(fileHandler)

    # Create console logger.
    stdHandler = logging.StreamHandler()
    stdFmt = logging.Formatter(CONSOLE_LOGGER_FORMAT)
    stdHandler.setFormatter(stdFmt)
    rootLogger.addHandler(stdHandler)

    # Set 'disabled' logger levels to ERROR to prevent
    # printing lower priority levels.
    for pkg in disable:
        tmpLogger = logging.getLogger(pkg)
        tmpLogger.setLevel(logging.ERROR)

    return rootLogger
