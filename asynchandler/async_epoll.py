#
# Copyright 2012 Alex Dementsov
#
# Uses two sockets: inet socket to listen on incoming requests and unix socket
# to delegate non-blocking request handling (e.g. logging) to a thread using epoll.
# 

import os
import errno
import select
import socket
import functools
import threading
import time

_EPOLLIN    = 0x001
_EPOLLERR   = 0x008
_EPOLLHUP   = 0x010

PORT        = 8080
HOST        = "127.0.0.1"
TIMEOUT     = 3600
SOCK_FLAGS  = socket.AI_PASSIVE | socket.AI_ADDRCONFIG
EPOLL_FLAGS = _EPOLLIN | _EPOLLERR | _EPOLLHUP
SOCK_NAME   = "/tmp/logger.sock"
counter     = 0     # global variable

class LoggerThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)
        
        
    def run(self):  
        sock    = get_server_socket()
        ep      = select.epoll()
        ep.register(sock.fileno(), EPOLL_FLAGS)         # register socket
        handler = functools.partial(conn_ready, sock)   # add handler for the socket

        events      = {}       
        while True:
            event_pairs = ep.poll(TIMEOUT)
            events.update(event_pairs)
            while events:
                fd, ev = events.popitem()
                try:
                    handler(fd, ev)
                except (OSError, IOError), e:
                    if e.args[0] == errno.EPIPE:
                        pass


def handle_connection(conn, address):
    "Handles connection"
    make_log(conn.recv(1024))
    

def conn_ready(sock, fd, ev):
    while True:
        try:
            conn, address = sock.accept()
        except socket.error, e:
            if e.args[0] not in (errno.EWOULDBLOCK, errno.EAGAIN):
                raise
            return
        conn.setblocking(0)
        handle_connection(conn, address)


# Unix socket
def get_server_socket(backlog=128):
    "Server for unix socket which listens for connections"
    sock    = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setblocking(0)
    try:
        os.unlink(SOCK_NAME)    # Clean up socket
    except:
        pass
    sock.bind(SOCK_NAME)
    sock.listen(backlog)
    return sock


def get_client_socket():
    "Client for unix socket"
    sock    = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    return sock


# Inet socket
def get_inet_socket(backlog=128):
    "Blocking inet socket"
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
    print "counter = %s" % counter
    print recv
    time.sleep(1)
    

def main():
    # Create Logger thread
    t   = LoggerThread()
    t.setDaemon(True)
    t.start()
    
    # Create server socket
    isock   = get_inet_socket()
    
    while True:
        # Get data from the inet client
        conn, addr  = isock.accept()
        recv    = conn.recv(1024)
        
        # Send received data to socket    
        sock    = get_client_socket()
        sock.connect(SOCK_NAME)
        sock.send(recv)
        sock.close()
    
        # Respond to the inet client
        conn.send("Doobie Doo")
        conn.close()
        
    isock.close()
        
    # Wait for the thread
    t.join()


if __name__ == "__main__":
    main()



