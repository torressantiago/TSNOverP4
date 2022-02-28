#!/bin/bash
# send
HOST=localhost
TASPORTPRI0=7777
TASPORTPRI1=6666

i=0

echo "Sending to: $HOST"

if [[ $# -ge 1 ]]
then
    while [[ $i -le 1000 ]]
    do
        if [[ $1 == "PRI0" ]]
        then
            echo "Message on port: $TASPORTPRI0 @date `date +%T.%6N`"
            echo "TAS" |nc -u $HOST $TASPORTPRI0
        elif [[ $1 == "PRI1" ]]
        then
            echo "Message on port: $TASPORTPR1 @date `date +%T.%6N`"
            echo "TAS" |nc -u $HOST $TASPORTPRI1
        else
            echo "TAS" |nc -u $HOST 80 # default to http
        fi
        let i++
    done
fi
