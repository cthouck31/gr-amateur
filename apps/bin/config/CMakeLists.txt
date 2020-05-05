set(APPS_CONFIG_DIR "~/.config/gr-amateur")

install(FILES
        AX25_Modem-HackRF-RTLSDR.ini
        DESTINATION ${APPS_CONFIG_DIR}
        COMPONENT config)
