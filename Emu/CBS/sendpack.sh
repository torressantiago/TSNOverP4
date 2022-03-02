#!/bin/bash
# send
HOST=192.168.0.200 # change with the respective port to be used as egress on bridge
PORTPRI0=7777
PORTPRI1=6666

test=`ls|grep 1GB.bin`
if [ -z "$test" ]
then
    wget https://speed.hetzner.de/1GB.bin
fi

i=0

echo "Sending to: $HOST"

while [[ $i -le 10 ]]
do
    # echo $i
    # echo $(($i % 2))
    echo "Message on port: $PORTPRI0 @date `date +%T.%6N`"
    nc -4u -w0 $HOST $PORTPRI0 < 1GB.bin
    let i++
done