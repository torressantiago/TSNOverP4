#!/bin/sh

brctl addbr br0
ip link set dev enp2s0f0 promisc on
ip link set dev enp2s0f1 promisc on
brctl addif br0 enp2s0f0
brctl addif br0 enp2s0f1
ip link set dev br0 up
iptables -t mangle -A POSTROUTING -p udp --dport 6666 -j CLASSIFY --set-class 0:1
iptables -t mangle -A POSTROUTING -p udp --dport 7777 -j CLASSIFY --set-class 0:0
modprobe br_netfilter
echo 1 > /proc/sys/net/bridge/bridge-nf-call-iptables
echo 1 > /proc/sys/net/bridge/bridge-nf-call-ip6tables
tc qdisc replace dev enp2s0f1 parent root handle 100 taprio \
num_tc 2 \
map 1 0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 \
queues 1@0 1@1 \
base-time 1554445635681310809 \
sched-entry S 01 800000 sched-entry S 02 200000 \
clockid CLOCK_TAI
