#!/bin/bash
# send
HOST=192.168.0.200 # change with the respective port to be used as egress on bridge
PORTPRI0=7777
PORTPRI1=6666

i=0

echo "Sending to: $HOST"

while [[ $i -le 1000 ]]
do
    if [[ $(($i % 2)) -eq 0 ]]
    then
        # echo $i
        # echo $(($i % 2))
        echo "Message on port: $PORTPRI0 @date `date +%T.%6N`"
        echo "TAS" |nc -4u -w0 $HOST $PORTPRI0
    else
        # echo $i
        echo "Message on port: $PORTPRI1 @date `date +%T.%6N`"
        echo "TAS" |nc -4u -w0 $HOST $PORTPRI1
    fi
    let i++
done