#!/bin/bash

APPS_PATH=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
APPS_SCRIPT=${APPS_PATH}/$(basename "${BASH_SOURCE[0]}")

GRCC=grcc
GRCC_FOUND=$(which ${GRCC})

# Check for 'grcc'.
if [[ ${GRCC_FOUND} = "" ]]; then
    echo "${GRCC} not found. Install 'gnuradio' using package manager or from source (http://github.com/gnuradio/gnuradio.git)."
    exit -1
fi

###########################################################
# Get all GRC files from 'hier'.
HIER_DIR="hier"
HIER_GRC=$(ls ${APPS_PATH}/${HIER_DIR}/*.grc)

# Compile all GRC files to Python.
echo "Preparing hierarchical blocks for installation..."
for f in ${HIER_GRC}; do
    OUT=$(grcc ${f} &> /dev/null)
done

# Compile all GRC files again (in case of embedded components).
echo "Compiling and installing..."
for f in ${HIER_GRC}; do
    echo "    Compiling '${HIER_DIR}/$(basename ${f})'..."
    OUT=$(grcc ${f})
done

###########################################################
# Get all GRC files from 'bin'.
BIN_DIR="bin"
BIN_GRC=$(ls ${APPS_PATH}/${BIN_DIR}/*.grc)

# Compile all GRC files to Python.
echo "Preparing applications for installation..."
# Compile all GRC files again (in case of embedded components).
echo "Compiling and installing..."
for f in ${BIN_GRC}; do
    echo "    Compiling '${BIN_DIR}/$(basename ${f})'..."
    OUT=$(grcc ${f} -d ${APPS_PATH}/${BIN_DIR})
done
