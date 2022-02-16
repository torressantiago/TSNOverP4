#!/usr/bin/env python
from socket import socket, AF_PACKET, SOCK_RAW
# raw socket on eth0
s = socket(AF_PACKET, SOCK_RAW)
s.bind(("eth0", 0))

# Source and destination address configuration
# TODO  Add a way to pass as parameter the source and destination
# H1 - H3
src_addr="\x08\x00\x00\x00\x01\x11"
dst_addr="\x08\x00\x00\x00\x04\x33"

# payload = string of 1000 '*'
payload=("*"*1000)

# no checksum = 0x00000000
checksum="\x00\x00\x00\x00"

# 0x0810 = VLAN
# TODO  Implement a way to send erroneous packets
ethertype="\x81\x00"

frame = dst_addr+src_addr+ethertype+payload+checksum

s.send(frame.encode())

s.close()


