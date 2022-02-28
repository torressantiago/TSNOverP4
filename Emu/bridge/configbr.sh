#!/bin/sh

test=`brctl show|grep br0`

if [ -z "$test" ]
then
    # -- Bridge config --
    # bridge interface creation
    brctl addbr br0

    # Set devices to promiscuous mode so that switching at L2 can be done
    ip link set dev enp2s0f0 promisc on
    ip link set dev enp2s0f1 promisc on

    # Add interfaces to bridge
    # NOTE once this is done, these interfaces are not usable for anything else
    brctl addif br0 enp2s0f0
    brctl addif br0 enp2s0f1

    # Bring up the interface
    ip link set dev br0 up
fi

# -- Switching configuration --
# Since a bridge works mostly on L2, the packet has to be modified so that tc (that works on higher levels) can schedule correctly
# Here the class is set according to the port used
# TODO to achieve real TSN behaviour, instead of ports, the VLAN tag must be used to set priority
iptables -t mangle -A POSTROUTING -p udp --dport 6666 -j CLASSIFY --set-class 0:1
iptables -t mangle -A POSTROUTING -p udp --dport 7777 -j CLASSIFY --set-class 0:0

# Configure the kernel to work according to the rules set by the iptables commands from above
modprobe br_netfilter
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo 1 > /proc/sys/net/bridge/bridge-nf-call-ip6tables

if [ $1 == "TAS" ]
then
    # Set the QoS rules for TAS
    tc qdisc replace dev enp2s0f1 parent root handle 100 taprio \
    num_tc 2 \
    map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 \
    queues 1@0 1@1 \
    base-time 1554445635681310809 \
    sched-entry S 01 800000 sched-entry S 02 200000 \
    clockid CLOCK_TAI

elif [ $1 == "CBS" ]
then
    sudo tc qdisc add dev eth0 parent root handle 200 mqprio \
        num_tc 3 \
        map 1 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 \
        queues 1@0 1@1 \
        hw 0

    # Q0
    sudo tc qdisc replace dev eth0 parent 200:1 cbs \
        idleslope 98688 sendslope -901312 hicredit 153 locredit -1389 \
        offload 1
    
    # Q1
    sudo tc qdisc replace dev eth0 parent 200:2 cbs \
        idleslope 3648 sendslope -996352 hicredit 12 locredit -113 \
        offload 1
fi