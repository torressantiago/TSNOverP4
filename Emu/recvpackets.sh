#!/bin/bash

PORT=$1
# Capture TAS
sudo tcpdump -w rawpackets -i lo port $PORT
sudo chown root rawpackets
sudo tcpdump -r rawpackets > packetdata
cut -b 1-16,48-51,67 packetdata > parsedpacketdata