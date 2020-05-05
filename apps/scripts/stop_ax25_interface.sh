#!/bin/bash

echo "Tearing down KISS adapter..."
killall kissattach
echo "Tearing down serial <--> TCP bridge..."
killall socat
