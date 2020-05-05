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

# Check for programs.
find_program(SOCAT_FOUND socat)
find_program(KISSATTACH_FOUND kissattach)
find_program(CHMOD_FOUND chmod)

include(GrPython)

if(SOCAT_FOUND)

    if(KISSATTACH_FOUND)

        if(CHMOD_FOUND)

        GR_PYTHON_INSTALL(
            PROGRAMS
            AX25_Interface_Manager.py
            DESTINATION bin
        )
        else(CHMOD_FOUND)
            message(STATUS "'chmod' command not found. Not adding 'AX25_Interface_Manager' script.")
        endif(CHMOD_FOUND)

    else(KISSATTACH_FOUND)
        message(STATUS "'kissattach' command not found. "
                       "Install 'ax25-tools' using package manager (sudo apt-get install ax25-tools). "
                       "Not adding 'AX25_Interface_Manager' script.")
    endif(KISSATTACH_FOUND)

else(SOCAT_FOUND)
    message(STATUS "'socat' command not found. "
                   "Install 'socat' using package manager (sudo apt-get install socat). "
                   "Not adding 'AX25_Interface_Manager' script.")
endif(SOCAT_FOUND)
