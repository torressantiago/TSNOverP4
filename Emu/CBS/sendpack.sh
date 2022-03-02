#!/bin/bash
# send
HOST=192.168.0.200 # change with the respective port to be used as egress on bridge
DEST=192.168.0.100
PORTPRI0=7777
PORTPRI1=6666

THREADS=100

iperf3 -c $HOST -B $DEST -p PORTPRI0 -t 60 --parallel $THREADS --udp