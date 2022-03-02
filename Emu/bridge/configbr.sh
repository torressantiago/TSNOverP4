#!/bin/sh

test=`brctl show|grep br0`

if [ -z "$test" ]
then
    # -- Bridge config --
    # bridge interface creation
    sudo brctl addbr br0

    # Set devices to promiscuous mode so that switching at L2 can be done
    sudo ip link set dev enp2s0f0 promisc on
    sudo ip link set dev enp2s0f1 promisc on

    # Add interfaces to bridge
    # NOTE once this is done, these interfaces are not usable for anything else
    sudo brctl addif br0 enp2s0f0
    sudo brctl addif br0 enp2s0f1

    # Bring up the interface
    sudo ip link set dev br0 up
fi

# -- Switching configuration --
# Since a bridge works mostly on L2, the packet has to be modified so that tc (that works on higher levels) can schedule correctly
# Here the class is set according to the port used
# TODO to achieve real TSN behaviour, instead of ports, the VLAN tag must be used to set priority
sudo iptables -t mangle -A POSTROUTING -p udp --dport 6666 -j CLASSIFY --set-class 0:1
sudo iptables -t mangle -A POSTROUTING -p udp --dport 7777 -j CLASSIFY --set-class 0:0

# Configure the kernel to work according to the rules set by the iptables commands from above
sudo modprobe br_netfilter
sudo echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
sudo echo 1 > /proc/sys/net/bridge/bridge-nf-call-ip6tables
: '
if [ $1 == "TAS" ]
then
    # Set the QoS rules for TAS
    tc qdisc replace dev enp2s0f1 parent root handle 100 taprio \
    num_tc 2 \
    map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 \
    queues 1@0 1@1 \
    base-time 1554445635681310809 \
    sched-entry S 01 80000000 sched-entry S 02 20000000 \
    clockid CLOCK_TAI

elif [ $1 == "CBS" ]
then
    # priority queue
    tc qdisc add dev enp2s0f1 handle 100: parent root mqprio num_tc 3 \
            map 2 2 1 0 2 2 2 2 2 2 2 2 2 2 2 2 \
            queues 1@0 1@1 2@2 \
            hw 0
    tc qdisc replace dev enp2s0f1 parent 100:4 cbs \
            locredit -8960000 hicredit 1380 sendslope -80000 idleslope 920000
    # These values are obtained from the following parameters,
    # idleslope is 920Mbit/s, the transmission rate is 1Gbit/s and the
    # maximum interfering frame size is 1500 bytes.
else
    # defaulting to TAS
    # Set the QoS rules for TAS
    tc qdisc replace dev enp2s0f1 parent root handle 100 taprio \
    num_tc 2 \
    map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 \
    queues 1@0 1@1 \
    base-time 1554445635681310809 \
    sched-entry S 01 80000000 sched-entry S 02 20000000 \
    clockid CLOCK_TAI
fi
'
# remember to update iproute2