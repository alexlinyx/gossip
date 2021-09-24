import socket
import random
import time
from typing import Type
import var
import update

#sends request every 3 sec to node in map
def blacklist_node(host, port):
    var.b_lock.acquire()
    if host!=var.HOST or port!=var.PORT: #cannot blacklist myself
        var.blacklist.add((host,port))
        try:
            del var.table[(host,port)]
        except:
            pass
        try:
            var.ip[host].remove(port)
        except:
            pass
    var.b_lock.release()

def connect_node(host, port):
    host = str(host)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        s.connect((host,port))
        data = s.recv(25600).decode(encoding='ascii') #should be more than enough for 256 lines at 100 bytes per line
    except socket.timeout: 
        blacklist_node(host, port)
        s.close()
        return
    except: 
        s.close()
        return
    s.close()
    update.update_map(data)

def start_client():
    while True:
        var.t_lock.acquire()
        keys = list(var.table.keys())
        var.t_lock.release()
        host,port = random.choice(keys)
        if host!=var.HOST or port!=var.PORT:
            connect_node(host, port)

        time.sleep(3)