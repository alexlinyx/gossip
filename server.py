import socket
import var
import update
import sys
import random
import time

#continuously listens of connections

def send_message(c, addr=None):
    if var.evil:
        host, port = update.parse_address(addr)
        msg = "{}:{},{},{}\n".format(host, port, sys.maxsize, sys.maxsize)
        c.send(msg.encode(encoding='ascii'))
        for p in range(2**16):
            msg1 = "{}:{}".format(host,p)
            msg2 = ",{},{}".format(sys.maxsize, 0)
            c.send(msg1.encode(encoding='ascii'))
            c.send(msg2.encode(encoding='ascii'))
            c.send('\n'.encode(encoding='ascii'))
        time.sleep(3)
    else:
        var.t_lock.acquire()
        for (host,port),(ts,digit) in var.table.items():
            msg = "{}:{},{},{}\n".format(host, port, ts, digit)
            c.send(msg.encode(encoding='ascii'))
        var.t_lock.release()

def listen_node(s):
    while True:
        conn, addr = s.accept()
        try:
            send_message(conn)
        except:
            pass
        conn.close()
        

def start_server(p):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',p))
    s.listen(50) #backlog 50
    return s