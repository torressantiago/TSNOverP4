#!/usr/bin/python3
from mininet.net import Mininet
from mininet.node import Node,Controller, RemoteController, OVSKernelSwitch, UserSwitch, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import Link, TCLink
from mininet.util import custom

QOS = 'TAS'

def topology():
    net = Mininet(controller = None, autoSetMacs = True)

    # Instantiate network members
    h1 = net.addHost('h1',mac='00:00:00:00:00:01')
    h2 = net.addHost('h2',mac='00:00:00:00:00:02')
    h3 = net.addHost('h3',mac='00:00:00:00:00:03')
    h4 = net.addHost('h4',mac='00:00:00:00:00:04')
    s1 = net.addSwitch('s1')

    # Create topology links
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s1)
    net.addLink(h4, s1)

    # Start the topology
    net.start()

    # Instantiate QoS rules
    # As per documented in http://www.openvswitch.org//support/dist-docs/ovs-vswitchd.conf.db.5.txt -> noop queue is used so that tc can configure the queue without trouble
    s1.cmd('sudo ovs-vsctl -- \
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
            --id=@q7 create queue other-config:min-rate=1')
    
    # Allowing L2/L3 switching
    s1.cmd('sudo ovs-ofctl add-flow s1 actions=output:normal')

    if QOS == 'TAS':
        # allow iptables to see the arriving packet so that it can modify it with the priority set in the PCP field
        # TODO  Do this with VLAN tag
        # class 0
        s1.cmd('sudo iptables -t mangle -A POSTROUTING -p udp --dport 7777 -j CLASSIFY --set-class 0:0')
        # class 1
        s1.cmd('sudo iptables -t mangle -A POSTROUTING -p udp --dport 6666 -j CLASSIFY --set-class 0:1')

        # Change queueing policy
        s1.cmd('sudo tc qdisc replace dev eth0 parent root handle 100 taprio \
                num_tc 3 \
                map 2 2 1 0 2 2 2 2 2 2 2 2 2 2 2 2 \
                queues 1@0 1@0 1@0 \
                base-time 1000000000 \
                sched-entry S 01 300000 \
                sched-entry S 03 300000 \
                sched-entry S 04 400000 \
                flags 0x1 \
                txtime-delay 500000 \
                clockid CLOCK_TAI')

    #elif QOS == 'CBS':
        # TODO  Do this with VLAN tag
        # class 0
        s1.cmd('sudo iptables -t mangle -A POSTROUTING -p udp --dport 7777 -j CLASSIFY --set-class 0:0')
        # class 1
        s1.cmd('sudo iptables -t mangle -A POSTROUTING -p udp --dport 6666 -j CLASSIFY --set-class 0:1')

        # Setting up the priority queue to mount CBS on
        s1.cmd('sudo tc qdisc add dev eth0 parent root handle 6666 mqprio \
                num_tc 3 \
                map 2 2 1 0 2 2 2 2 2 2 2 2 2 2 2 2 \
                queues 1@0 1@1 2@2 \
                hw 0')

        # Use intel provided code to compute CBS parameters
        s1.cmd('sudo tc qdisc replace dev eth0 parent 6666:1 cbs \
                idleslope 98688 sendslope -901312 hicredit 153 locredit -1389 \
                offload 1')

        s1.cmd('sudo tc qdisc replace dev eth0 parent 6666:2 cbs \
                idleslope 3648 sendslope -996352 hicredit 12 locredit -113 \
                offload 1')
    else:
        print("No QoS rule chosen, defaulting to noop")

    
    # Test connectivity between hosts
    print (h1.cmd( 'ping -c1', h4.IP() ))

    CLI(net)

    net.stop()


if __name__ == '__main__':
    # setLogLevel( 'info' )
    topology()