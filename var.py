#global variables

table = {('127.0.0.1', 1):(100, 1), ('127.0.0.1', 23):(100, 5)} # host,port: timestamp, digit
ip = {'127.0.0.1':{1,23}} # ip: list of ports, newest to cold
blacklist = set() #set of bad nodes

#server socket
#create new socket each time for connection?

HOST = '127.0.0.1'
PORT = 1

def init_ip(host, port):
    global HOST 
    HOST = host
    global PORT 
    PORT = port