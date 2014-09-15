#!/usr/bin/env python
import csv
from ipaddr import IPv4Address, IPv4Network
from optparse import OptionParser    

networks = set()

def to_24s(prefix):
    # for the love of god don't process 0.0.0.0/0
    
    if str(prefix) in networks:
        return
    else:
        networks.add(str(prefix))

    if prefix.prefixlen == 0:
        return

    if prefix.prefixlen < 24:
        subnet_list = prefix.subnet()
        for subnet in subnet_list:
            to_24s(subnet)
    else:
        print(prefix.network)

def all_24s(prefix, _24_list):
    #return a list of /24s advertised by this bgp prefix
    
    if prefix.prefixlen == 0:
        return

    if prefix.prefixlen < 24:
        subnet_list = prefix.subnet()
        for subnet in subnet_list:
            all_24s(subnet, _24_list)
    else:
        _24_list.append(str(prefix.network))


def main():
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='in_file', help='read input from FILE', metavar='FILE')
    (options, args) = parser.parse_args()

    bgpdump_reader = csv.reader(open(options.in_file, 'rb'), delimiter='|')
    
    address_set = set()

    for row in bgpdump_reader:
        prefix = IPv4Network(row[5])
    
        if prefix in address_set:
            continue
        
        """
        #this block prints out all the /24s advertised by a particular AS
        path = row[6].split(' ')
        if path is None or len(path) == 0:
            continue

        asn = path[len(path)-1]

        prefix_list = list()
        all_24s(prefix, prefix_list)
        
        _24s = ' '.join(prefix_list)
        print(asn+' '+str(prefix)+' '+_24s)

        address_set.add(prefix)
        """

        """
        #this block prints out the advertised prefix and then all the /24s from it on a line
        prefix_list = list()
        all_24s(prefix, prefix_list)
        
        prefix_list.insert(0, str(prefix))
        
        line = ' '.join(prefix_list)
        print(line) 
        
        address_set.add(prefix)
        """

        to_24s(prefix) #this was the original bit for unravelling the /24s. it prints one per line

if __name__ == '__main__':
    main()
