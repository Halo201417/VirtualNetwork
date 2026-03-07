from mininet.net import Mininet
from mininet.node import Node
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel, info

def run_topology():
    net = Mininet(topo=None, build=False, link=TCLink)
    
    info('Adding Nodes\n')
    
    #Final nodes + default gateway
    h1 = net.addHost('h1', ip='10.0.1.2/24', defaultRoute='via 10.0.1.1')
    h2 = net.addHost('h2', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1')
    
    #Adding the router
    r1 = net.addHost('r1', ip='10.0.1.1/24')
    
    info('Creating links\n')
    
    #Client h1 to router r1
    net.addLink(h1, r1, intfName2='r1-eth1', params2={'ip':'10.0.1.1/24'})
    
    #Router r1 to server h2
    net.addLink(r1, h2, intfName='r1-eth2', params1={'ip':'10.0.2.1/24'}, loss=4, delay='5ms', bw=10)
    
    info('Starting Network\n')
    net.start()
    
    info('Converting r1 into the router')
    r1.cmd('sysctl net.ipv4.ip_forward=1')
    
    info('Opening CLI\n')
    CLI(net)
    
    info('Stopping the network and cleaning\n')
    r1.cmd('sysctl net.ipv4.ip_forward=0')
    net.stop()
    
if __name__ == "__main__":
    setLogLevel('info')
    run_topology()