#!/usr/bin/python2
from socket import socket, AF_PACKET, SOCK_RAW
import sys
# Source and destination address configuration
if len(sys.argv) > 1:
    if sys.argv[1] == "correct":
        # H1 - H3
        src_addr="\x08\x00\x00\x00\x01\x11"
        dst_addr="\x08\x00\x00\x00\x03\x33"

        # 0x8100 = VLAN
        ethertype="\x81\x00"

    elif sys.argv[1] == "incorrect_ethertype":
        # H1 - H3
        src_addr="\x08\x00\x00\x00\x01\x11"
        dst_addr="\x08\x00\x00\x00\x03\x33"

        # 0x0800 = IPv4
        ethertype="\x08\x00"

    elif sys.argv[1] == "incorrect_dst_addr":
        # H1 - H3
        src_addr="\x08\x00\x00\x00\x01\x11"
        dst_addr="\x08\x00\x00\x00\x04\x44"

        # 0x0800 = IPv4
        ethertype="\x81\x00"

    elif sys.argv[1] == "incorrect_src_addr":
        # H1 - H3
        src_addr="\x08\x00\x00\x00\x04\x44"
        dst_addr="\x08\x00\x00\x00\x03\x33"

        # 0x0800 = IPv4
        ethertype="\x81\x00"

    elif sys.argv[1] == "help":
        print("correct - sends correct source @, destination @ and ethertype. \
            \nincorrect_etherype - sends incorrect ethertype, but correct source and destination @. \
            \nincorrect_dst_addr - sends incorrect destination @, but correct source address and ethertype. \
            \nincorrect_src_addr - sends incorrect source @, but correct destination @ and ethertype.")
        sys.exit()

    else:
        # H1 - H3
        src_addr="\x08\x00\x00\x00\x01\x11"
        dst_addr="\x08\x00\x00\x00\x03\x33"

        # 0x8100 = VLAN
        ethertype="\x81\x00"

else:
    # H1 - H3
    src_addr="\x08\x00\x00\x00\x01\x11"
    dst_addr="\x08\x00\x00\x00\x03\x33"

    # 0x8100 = VLAN
    ethertype="\x81\x00"

# raw socket on eth0
s = socket(AF_PACKET, SOCK_RAW)
s.bind(("eth0", 0))

# payload = string of 1000 '*'
payload=("*"*1000)

# no checksum = 0x00000000
checksum="\x00\x00\x00\x00"



frame = dst_addr+src_addr+ethertype+payload+checksum
print(dst_addr,src_addr,ethertype,payload,checksum)

s.send(frame)

s.close()


