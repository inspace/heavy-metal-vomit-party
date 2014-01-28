import subprocess
import socket
import time
import sys
import ipaddr
from os.path import expanduser

class Mapper(object):
    
    def __init__(self, iplane_file=None, ixp_file=None):
        import SubnetTree

        self.iplane_file = iplane_file if iplane_file else expanduser('~/weekly_origin_as_mapping.txt')  
        self.ixp_file = ixp_file if ixp_file else expanduser('~/ip_city_country.pl') 
        self.__private_prefixes = ('10.', '192.168', '0.0.0.0/0', '172.16.', '172.17.', '172.18.', '172.19.', '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.', '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.')
        self.tree = SubnetTree.SubnetTree()
        self.load()

    def load(self):
        import time       
 
        f = open(self.iplane_file)
        for line in f:
            line = line.rstrip()
            try:
                chunks = line.split() 
                prefix = chunks[0]
                asn = chunks[1]
            
                if prefix.startswith(self.__private_prefixes):
                    continue

                self.tree[prefix] = asn
            except:
                #sys.stderr.write(self.iplane_file+': Couldn\'t parse line: %s\n' % line) 
                pass
        f.close()

        f = open(self.ixp_file)
        for line in f:
            #no need to strip
            try:
                chunks = line.split()
                prefix = chunks[0]

                if prefix.startswith(self.__private_prefixes):
                    continue

                self.tree[prefix] = 'IXP'
            except:
                #sys.stderr.write(self.ixp_file+': Couldn\'t parse line %s\n' % line)
                pass
        f.close()

    def mapIp(self, ip):
        
        if ip.startswith(self.__private_prefixes):
            return 'NA'

        try:
            return self.tree[ip]
        except KeyError:
            return 'NA'        

    def mapTrace(self, trace):
        new_trace = []
        for ip in trace:
            new_as = self.mapIp(ip)
            
            if new_as != 'NA' and new_as != 'IXP':
                if not new_trace:
                    new_trace.append(new_as)
                elif new_trace[-1] != new_as:
                    new_trace.append(new_as)

        return new_trace

    def as2ipMap(self, trace):
        new_map = {}
        for ip in trace:
            asn = self.mapIp(ip)
            try:
                new_map[asn].append(ip)
            except:
                new_map[asn] = [ip]
        return new_map
    
    def is_private(self, prefix):
        if prefix.startswith(self.__private_prefixes):
            return True
        return False
