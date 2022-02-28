#!/bin/bash

# Capture packets
sudo tcpdump -w rawpackets -i enp2s0f0 port '(7777 or 6666)'
sudo chown root rawpackets
sudo tcpdump -r rawpackets > packetdata
cut -b 1-16,51-54 packetdata > parsedpacketdata