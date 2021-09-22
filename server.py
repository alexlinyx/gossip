#continuously listens of connections

import socket
import var
           

def listen_node(s):
    while True:
        conn, addr = s.accept()
        print ('Got connection from', addr)
        for (host,port),(time,digit) in var.table.items():
            msg = "{}:{},{},{}\n".format(host, port, time, digit)
            conn.send(msg.encode(encoding='ascii'))
        conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('',var.PORT)) #socket.gethostname() for ip?
    s.listen(30) #backlog 30
    #s = socket.create_server(address=(var.HOST,var.PORT), backlog=30) 
    listen_node(s)
    s.close()