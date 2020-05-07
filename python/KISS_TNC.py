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

import os
import logging
logger = logging.getLogger(__name__)

import numpy as np
import threading
from Queue import Queue
import time
import pmt
from gnuradio import gr
import KISS_Utils
from KISS_Utils import KISS_pack, KISS_unpack


class KISS_TNC(gr.sync_block):
    """
    docstring for block KISS_TNC
    """
    def __init__(self, bitrate=1200.0, numPreambles=1, numPostambles=1, portNum=0, csma=True):
        gr.sync_block.__init__(self,
            name="KISS_TNC",
            in_sig=[np.uint8] if csma else None,
            out_sig=None)

        # Save bit rate and preamble count.
        self.Rb      = float(bitrate)
        self.numPre  = int(numPreambles)
        self.numPost = int(numPostambles)
        self.portNum = int(portNum)
        self.csma    = csma

        # Set to defaults.
        self.dspLock = threading.Lock()
        self.lock    = threading.Lock()
        self.txQueue = Queue()
        self.reset()

        # TNC -> Modem.
        self.message_port_register_in(pmt.intern("tnc_req"))
        self.message_port_register_out(pmt.intern("modem_req"))
        self.message_port_register_out(pmt.intern("modem_data"))
        self.set_msg_handler(pmt.intern("tnc_req"), self._tncInputHandler)
        # Modem -> TNC.
        self.message_port_register_in(pmt.intern("modem_resp"))
        self.message_port_register_out(pmt.intern("tnc_resp"))
        self.set_msg_handler(pmt.intern("modem_resp"), self._modemInputHandler)

        # Control handlers.
        self.handler = {
            KISS_Utils.KISS_CTRL_DATA       : self.setData,
            KISS_Utils.KISS_CTRL_TXDELAY    : self.setTxDelay,
            KISS_Utils.KISS_CTRL_P          : self.setPersistence,
            KISS_Utils.KISS_CTRL_SLOTTIME   : self.setSlotInterval,
            KISS_Utils.KISS_CTRL_TXTAIL     : self.setTxTail,
            KISS_Utils.KISS_CTRL_FULLDUPLEX : self.setFullDuplex,
            KISS_Utils.KISS_CTRL_RETURN     : self.setPassthrough,
        }

        # Debug.
        logger.debug("Created KISS TNC component (baud=%.1f,preambles=%u,postambles=%u,port=%u,csma=%s)." %
                     (self.Rb, self.numPre, self.numPost, self.portNum, str(self.csma)))

    def reset(self):
        """
        Reset TNC to default settings.
        """
        with self.lock:
            self.txDelay     = 100.0
            self.persistence = 0.25
            self.slotIntvl   = 100.0
            self.txTail      = 500.0
            self.fullDuplex  = False
            self.passthrough = False
            self.carrTimeout = 30.0
            self.carrElapsed = 0.0
            while not self.txQueue.empty():
                self.txQueue.get()

        with self.dspLock:
            self.carrSense = False

    def _tncInputHandler(self, msg):
        # Parse raw packet.
        if not pmt.is_pair(msg):
            logger.error("KISS_TNC: Invalid input message.")
            return

        value = pmt.cdr(msg)
        if not pmt.is_u8vector(value):
            logger.error("KISS_TNC: Invalid message type.")
            return

        # Get bytes.
        data = bytearray(pmt.to_python(value))
        # Unpack to frame.
        frames = KISS_unpack(data)
        if len(frames) == 0:
            logger.error("Failed to unpack KISS frames from data: %s" % str(data))
            return

        # Filter out TNC commands to different port(s).
        filtered = []
        for frame in frames:
            port = frame.get("port", -1)
            if port != self.portNum:
                logger.debug("Filtering KISS packet (port %u != %u)." %
                             (port, self.portNum))
                continue
            filtered.append(frame)

        # Perform the desired operation.
        for frame in filtered:
            # Get control byte.
            ctrl = frame.get("ctrl", None)
            if ctrl == None:
                logger.error("No control byte found.")
                continue

            # Call correct handler.
            handler = self.handler.get(ctrl, self.printError)
            handler(frame)

            # Add data to transmit queue.
            octets = frame.get("data", [])
            if len(octets) > 0:
                logger.debug("Queueing packet (len=%u)." % len(octets))
                self.txQueue.put(octets)

        # Send data immediately if CSMA is disabled.
        if not self.csma:
            self.sendData()

    def sendData(self, csense=False):
        stop = threading.Event()
        while (not self.txQueue.empty()) and (not stop.isSet()):
            data = self.txQueue.get()
            # Empty data field.
            if len(data) == 0:
                logger.debug("Empty packet detected, not transmitting.")
                return

            # Check if passthrough is enabled (no modem control).
            if self.passthrough:
                logger.debug("Passthrough packet transmitted!")
                self.message_port_pub(pmt.intern("modem_data"),
                                      pmt.cons(pmt.PMT_NIL,
                                               pmt.init_u8vector(len(data), data)))
                return

            # Compute burst information.
            numBits   = self.numPre*8 + len(data)*8 + self.numPost*8
            burstTime = self.txDelay*1e-3 + float(numBits)/self.Rb + self.txTail*1e-3

            start  = time.time()
            while 1:
                # Wait for carrier detection to unlock.
                if csense:
                    logger.debug("Carrier detected, sleeping...")
                    # Put data back into queue.
                    self.txQueue.put(data)
                    # Break out of transmit and check for carrier again.
                    stop.set()
                    break

                # Persistance value from 0 to 1.
                prob = np.random.uniform()
                if prob > self.persistence:
                    # Reset carrier timeout.
                    start = time.time()
                    logger.debug("Persistence threshold violated, sleeping for slot interval...")
                    time.sleep(self.slotIntvl*1e-3)
                    continue

                logger.debug("Turning down RX gain.")
                self.message_port_pub(pmt.intern("modem_req"),
                                      pmt.cons(pmt.intern("gain"), pmt.from_float(0.0)))

                logger.debug("Transmitting packet!")
                # Delay for TX delay.
                time.sleep(self.txDelay*1e-3)

                # Send chunk.
                self.message_port_pub(pmt.intern("modem_data"),
                                      pmt.cons(pmt.PMT_NIL,
                                               pmt.init_u8vector(len(data), data)))

                # Delay for theoretical burst time plus TX tail.
                # This is the best approximation as there is no back pressure.
                logger.debug("Sending burst ({:1f} msec)...".format(burstTime*1e3))
                time.sleep(burstTime)

                self.message_port_pub(pmt.intern("modem_req"),
                                      pmt.cons(pmt.intern("gain"), pmt.from_float(40.0)))

                break

    def setData(self, frame):
        pass

    def setTxDelay(self, frame):
        current      = KISS_msecToByte(self.txDelay)
        txDelay      = frame.get("param", current)
        self.txDelay = KISS_byteToMsec(txDelay)

    def setPersistence(self, frame):
        current          = KISS_P_floatToInt(self.persistence)
        persistence      = frame.get("param", current)
        self.persistence = KISS_P_intToFloat(persistence)

    def setSlotInterval(self, frame):
        current        = KISS_msecToByte(self.slotIntvl)
        slotIntvl      = frame.get("param", current)
        self.slotIntvl = KISS_byteToMsec(slotIntvl)

    def setTxTail(self, frame):
        current     = KISS_msecToByte(self.txTail)
        txTail      = frame.get("param", current)
        self.txTail = KISS_byteToMsec(txTail)

    def setFullDuplex(self, frame):
        self.fullDuplex = bool(frame.get("param", self.fullDuplex))

    def setPassthrough(self, data):
        self.passthrough = bool(frame.get("param", self.passthrough))

    def printError(self, frame):
        logger.error("Invalid frame decoded: %s" % str(frame))
        return

    def _modemInputHandler(self, msg):
        # Parse raw packet.
        if not pmt.is_pair(msg):
            logger.error("KISS_TNC: Invalid input message.")
            return

        value = pmt.cdr(msg)
        if not pmt.is_u8vector(value):
            logger.error("KISS_TNC: Invalid message type.")
            return

        # Get bytes.
        data   = bytearray(pmt.to_python(value))
        frame  = {"ctrl": KISS_Utils.KISS_CTRL_DATA, "port": self.portNum, "param": 0, "data": data}
        packet = KISS_pack(frame)

        # Send TNC response.
        self.message_port_pub(pmt.intern("tnc_resp"),
                              pmt.cons(pmt.PMT_NIL,
                                       pmt.init_u8vector(len(packet), packet)))

    def work(self, input_items, output_items):
        in0 = input_items[0]
        with self.dspLock:
            self.carrSense = np.count_nonzero(in0)

        # Send data.
        self.sendData(self.carrSense)

        return len(in0)

