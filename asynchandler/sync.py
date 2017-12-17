#
# Copyright 2012 Alex Dementsov
#
# Uses inet socket to listen on incoming requests to perform blocking request
# handling (e.g. logging).
# 

import os
import socket
import threading
import time

PORT        = 8080
HOST        = "127.0.0.1"
SOCK_FLAGS  = socket.AI_PASSIVE | socket.AI_ADDRCONFIG
counter     = 0     # global variable

def get_inet_socket(backlog=128):
    "Blocking socket"
    res     = socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM, 0, SOCK_FLAGS)
    af, socktype, proto, canonname, sockaddr = res[0]
    sock    = socket.socket(af, socktype, proto)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(sockaddr)
    sock.listen(backlog)
    return sock    


def make_log(recv):
    "Perform logging"
    global counter
    counter  += 1
    print "num = %s" % counter
    print recv
    time.sleep(1)


def main():
    # Create server socket
    isock   = get_inet_socket()
    
    while True:
        # Get data from the inet client
        conn, addr  = isock.accept()
        recv    = conn.recv(1024)
        
        # Blocking request handling
        make_log(recv)
        
        # Respond to the inet client
        conn.send("Doobie Doo")
        conn.close()
        
    isock.close()
    
    
if __name__ == "__main__":
    main()