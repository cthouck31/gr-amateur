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

# Application list.
set(APP_SRCS ${APP_SRCS}
    AX25_Modem.grc
    AX25_Modem_GUI.grc)

# Application Python list.

# Check for 'grcc'.
find_program(GRCC_FOUND grcc)

if (GRCC_FOUND)
    # Generate all components.
    foreach(APP_GRC ${APP_SRCS})
        # Compile using GRCC.
        message(STATUS "    Updating using '${APP_GRC}'...")
        execute_process(COMMAND grcc -d ./ ${APP_GRC}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
        # Get generated name.
        string(REGEX REPLACE "[.]grc$" ".py" APP_PROG ${APP_GRC})
        message(STATUS "        ${APP_GRC} -> ${APP_PROG}")
        # Add Python program to list of applications.
        set(APP_PROGS ${APP_PROGS} ${APP_PROG})
    endforeach()
else(GRCC_FOUND)
    message(FATAL_ERROR "'grcc' command not found (included in 'gnuradio' package). "
                        "Needed to compile applications for this module.")
endif(GRCC_FOUND)

include(GrPython)
GR_PYTHON_INSTALL(
    PROGRAMS
    ${APP_PROGS}
    DESTINATION bin
)

# Add configuration files.
add_subdirectory(config)
