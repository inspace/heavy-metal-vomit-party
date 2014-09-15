import socket

def validip(ip):
    try:
        socket.inet_aton(addr)
        return true
    except socket.error:
        return false

def fix_asn(asn):

    #deal with MOAS
    if '_' in asn:
        asn = asn.split('_')[0] #take the first    

    #don't know why these braces are in here
    if asn[0] == '{' and asn[-1] == '}':
        asn = asn[1:-2]

    #deal with > 16-bit ASNs
    if '.' in asn:
        asnbytes = asn.split('.')
        higher2bytes = int(asnbytes[0])
        lower2bytes = int(asnbytes[1])
        asn_int = higher2bytes*65536 + lower2bytes
        asn = str(asn_int)

    return asn

def to24(ip):
    return ip[:ip.rfind('.')+1]+'0'

def all_24s():

    for first in range(1, 256):
        if first == 10:
             continue
        for second in range(0, 256):
            if first == 192 and second == 168:
                continue
            if first == 172 and (second >= 16 and second <= 31):
                continue
 
            for third in range(0, 256):
                address = '%d.%d.%d.0' % (first, second, third)
                yield address
