#!/bin/bash
PORTPRI0=7777
iperf3 -s -p $PORTPRI0 -J > packetdata.json