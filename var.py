from threading import Lock

#global variables
table = {}
ip = {}
blacklist = set() #set of bad nodes
evil = False

t_lock, ip_lock, b_lock = Lock(), Lock(), Lock() #locks for table, ip, and blacklist

HOST = ''
PORT = 0

def init_ip(host, port):
    global HOST 
    HOST = host
    global PORT 
    PORT = port
    global table
    table = {(HOST,PORT):0} #placeholder for client