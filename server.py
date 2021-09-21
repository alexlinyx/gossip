#continuously listens of connections

import main
import client
import input
import socket            

def listen_node():
    s = socket.create_server(address=(main.HOST,main.PORT), backlog=30) 
    
    while True:
        conn, _ = s.accept()
        for (host,port),(time,digit) in main.table.keys():
            msg = "{}:{},{},{}".format(host, port, time, digit)
            conn.send(msg.encode(encoding='ascii'))
        conn.close()
