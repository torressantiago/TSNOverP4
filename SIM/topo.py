#!/usr/bin/python3

"""simple switch topology to run

router between two subnets:

   h1----+
         |
         r ---- h3
         |
   h2----+
"""
from mininet.net import Mininet
from mininet.node import Node, OVSKernelSwitch, Controller, RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.topo import Topo
from mininet.log import setLogLevel, info

" These are to test prior to static switching "
#h1addr = '10.0.1.2/24'
#h2addr = '10.0.2.2/24'
#h4addr = '10.0.4.2/24'
#r1addr1= '10.0.1.1/24'
#r1addr2= '10.0.2.1/24'
#r1addr4= '10.0.4.1/24'

class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable forwarding on the router
        info ('enabling forwarding on ', self)
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class RTopo(Topo):

    def build(self, **_opts):     # special names?
        defaultIP = '10.0.1.1/24'  # IP address for r0-eth1
        r  = self.addNode( 'r', cls=LinuxRouter) # , ip=defaultIP )
        h1 = self.addHost( 'h1', ip='10.0.1.10/24', defaultRoute='via 10.0.1.1' )
        h2 = self.addHost( 'h2', ip='10.0.2.10/24', defaultRoute='via 10.0.2.1' )
        h4 = self.addHost( 'h3', ip='10.0.3.10/24', defaultRoute='via 10.0.3.1' )
 
        # Oct 2020: the params2 method for setting IPv4 addresses
        # doesn't always work; see below
        self.addLink( h1, r, intfName1 = 'h1-eth', intfName2 = 'r-eth1', params2 = {'ip' : '10.0.1.1/24'})

        self.addLink( h2, r, intfName1 = 'h2-eth', intfName2 = 'r-eth2', params2 = {'ip' : '10.0.2.1/24'})
                 
        #self.addLink( r, h4, intfName2 = 'h4-eth', intfName1 = 'r-eth4', delay='10ms')
        self.addLink( r, h4, intfName2 = 'h3-eth', intfName1 = 'r-eth3', params2 = {'ip' : '10.0.2.1/24'})
                 
# delay is the ONE-WAY delay, and is applied only to traffic departing h4-eth.

def main():
    rtopo = RTopo()
    net = Mininet(topo = rtopo,
                  link=TCLink,
                  #switch = OVSKernelSwitch,                   #controller = RemoteController,
        	  autoSetMacs = True   # --mac
                )  
    net.start()
    r = net['r']
    r.cmd('ip route list');
    # r's IPv4 addresses are set here, not above.
    r.cmd('ifconfig r-eth1 10.0.1.1/24')
    r.cmd('ifconfig r-eth2 10.0.2.1/24')
    r.cmd('ifconfig r-eth3 10.0.4.1/24')
    r.cmd('sysctl net.ipv4.ip_forward=1')
    " Enter command to change queuing algorithm"
    # r.cmd('tc qdisc change dev r-eth4 handle 10: netem  delay {} limit {}'.format(DELAYstr, QUEUE))

    h1 = net['h1']
    h2 = net['h2']
    h3 = net['h3']

    for h in [r, h1, h2, h3]: h.cmd('/usr/sbin/sshd')

    CLI( net)
    net.stop()

setLogLevel('debug')
main()

"""
This leads to a queuing hierarchy on r with an htb node, 5:0, as the root qdisc. 
The class below it is 5:1. Below that is a netem qdisc with handle 10:, with delay 110.0ms.
We can change the limit (maximum queue capacity) with:

	tc qdisc change dev r-eth1 handle 10: netem limit 5 delay 110.0ms
	tc qdisc change dev r-eth1 handle 10: netem delay 700ms

"""
