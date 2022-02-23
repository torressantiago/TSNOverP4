#!/bin/bash

# This allows to merge root and p4 X domains and therefore execute wireshark as root
xauth extract - $DISPLAY | sudo xauth merge -
