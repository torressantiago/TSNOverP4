#!/bin/bash
sudo mn -c
sudo ovs-vsctl clear port s1-eth1 qos
sudo ovs-vsctl clear port s1-eth2 qos
sudo ovs-vsctl clear port s1-eth3 qos
sudo ovs-vsctl clear port s1-eth4 qos
sudo ovs-vsctl --all destroy qos
sudo ovs-vsctl --all destroy queue  