# Hier block list.
set(APP_HIER_SRCS ${APP_HIER_SRCS}
    AFSK_Demodulator_BPF.grc
    AX25_AFSK1200_Demodulator.grc
    AX25_AFSK1200_Modulator.grc
    AX25_Deframer.grc
    AX25_Framer.grc
    Digital_Down_Converter.grc
    Digital_Up_Converter.grc)


# Check for 'grcc'.
find_program(GRCC_FOUND grcc)

if (GRCC_FOUND)
    # Generate all components.
    foreach(HIER_GRC ${APP_HIER_SRCS})
        message(STATUS "    Compiling '${HIER_GRC}'...")
        execute_process(COMMAND grcc ${HIER_GRC}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
    endforeach()
    # Run again to include all components that are
    # sub-components in custom flow-graphs (i.e. a custom component
    # inside of a custom component).
    foreach(HIER_GRC ${APP_HIER_SRCS})
        message(STATUS "    Compiling '${HIER_GRC}'...")
        execute_process(COMMAND grcc ${HIER_GRC}
            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
    endforeach()

else(GRCC_FOUND)
    message(FATAL_ERROR "'grcc' command not found (included in 'gnuradio' package). "
                        "Needed to compile hier blocks for this module.")
endif(GRCC_FOUND)
