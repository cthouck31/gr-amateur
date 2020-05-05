# Copyright 2011 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# GNU Radio is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# GNU Radio is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GNU Radio; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
install(FILES
    AX25_Packet_Encoder.xml
    Tagged_Nrzi_Encoder.xml
    Saturated_Counter.xml
    Burst_Stager.xml
    Burst_Injector.xml
    Tagged_Stream_Add_Length_Tag.xml
    AX25_Packet_Decoder.xml
    AX25_Packet_Formatter.xml
    #    amateur_AX25_AFSK_Transmitter.xml
    #    amateur_AFSK_Demodulator_BPF.xml
    #    amateur_AX25_AFSK_Receiver.xml
    AFSK_Modulator.xml
    KISS_TNC.xml
    qtgui_Terminal_Sink.xml
    qtgui_Embedded_Terminal.xml
    Message_To_Json.xml
    DESTINATION share/gnuradio/grc/blocks
)
