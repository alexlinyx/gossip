import socket
import random
import time
from typing import Type
import var
import update

#sends request every 3 sec to node in map
def blacklist_node(host, port):
    var.blacklist.add((host,port))
    try:
        del var.table[(host,port)]
    except KeyError:
        pass
    try:
        var.ip[host].remove(port)
    except KeyError:
        pass

def connect_node(host, port):
    #set up connection
    host = str(host)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((host,port))
        data = s.recv(2560).decode(encoding='ascii') #assuming each line is less than 10 bytes
    except socket.timeout: #ConnectionRefusedError
        #blacklist_node(host, port)
        print('socket timeout')
        s.close()
        return
    except ConnectionRefusedError:
        print('connection error')
        s.close()
        return

    s.close()
    update.update_map(data)

def start_client():
    while True:
        if len(var.table)>1:
            keys = list(var.table.keys())
            host,port = random.choice(keys)
            while host==var.HOST and port==var.PORT:
                host,port = random.choice(keys)
            connect_node(host, port)

        print('Attempted connection')
        time.sleep(3)