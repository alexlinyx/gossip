import socket
import var
import update
import sys
import random

#continuously listens of connections
           
def listen_node(s):
    while True:
        conn, addr = s.accept()
        if var.evil:
            host, port = update.parse_address(addr)
            conn.send(''.encode(encoding='ascii'))
            msg = "{}:{},{},{}\n".format(host, port, sys.maxsize, 0.0)
            for i in range(256):
                conn.send(msg.encode(encoding='ascii'))
            continue #continues without closing, cannot run adverserial mode for long before backlog is full
        
        var.t_lock.acquire()

        for (host,port),(time,digit) in var.table.items():
            msg = "{}:{},{},{}\n".format(host, port, time, digit)
            conn.send(msg.encode(encoding='ascii'))

        var.t_lock.release()
        conn.close()
        

def start_server(p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',p))
    s.listen(50) #backlog 50
    return s