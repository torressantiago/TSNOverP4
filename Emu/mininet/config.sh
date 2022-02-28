#!/bin/bash
# Instantiate QoS rules
sudo ovs-vsctl -- \
      set port s1-eth4 qos=@newqos -- \
      --id=@newqos create qos type=linux-noop \
      other-config:min-rate=1 \
      queues:1=@q1 \
      queues:2=@q2 \
      queues:3=@q3 \
      queues:4=@q4 \
      queues:5=@q5 \
      queues:6=@q6 \
      queues:7=@q7 -- \
      --id=@q1 create queue other-config:min-rate=1 -- \
      --id=@q2 create queue other-config:min-rate=1 -- \
      --id=@q3 create queue other-config:min-rate=1 -- \
      --id=@q4 create queue other-config:min-rate=1 -- \
      --id=@q5 create queue other-config:min-rate=1 -- \
      --id=@q6 create queue other-config:min-rate=1 -- \
      --id=@q7 create queue other-config:min-rate=1


# Adding rules as flows
# sudo ovs-ofctl add-flow s1 in_port=s1-eth1,actions=set_queue:1,normal
# sudo ovs-ofctl add-flow s1 in_port=s1-eth2,actions=set_queue:2,normal
# sudo ovs-ofctl add-flow s1 in_port=s1-eth3,actions=set_queue:3,normal