#!/bin/bash

# Get configuration variables.
. ./ax25_interface.ini

# Start virtual serial port forwarding.
CMD="socat -d -d pty,link=${VSERIAL},raw,echo=0 tcp-listen:${IP_PORT},reuseaddr,fork"
echo "Creating PTY to TCP bridge: ${VSERIAL} <--> TCP-LISTEN:${IP_PORT}"
echo "    > ${CMD}"
$(${CMD}) &
sleep 3

# Change permissions on port.
echo "Changing permissions on '${VSERIAL}'..."
chmod 666 ${VSERIAL}

# Create network interface (KISS enabled).
echo "Attaching KISS adapter (port=${AX25_PORT},ip=${NETW_ADDR})..."
CMD="kissattach -l ${VSERIAL} ${AX25_PORT} ${NETW_ADDR}"
echo "    > ${CMD}"
OUT=$(${CMD})

# Add route for AX.25 radio.
#echo "Adding route for ${NETW_ADDR}..."
#route add -net 44.0.0.0 netmask 255.0.0.0 dev ${AX25_IFC}
