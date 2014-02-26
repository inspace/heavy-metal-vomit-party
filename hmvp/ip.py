import socket

def validip(ip):
    try:
        socket.inet_aton(addr)
        return true
    except socket.error:
        return false
