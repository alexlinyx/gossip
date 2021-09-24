import ipaddress
from datetime import datetime
import var
import client
import update

#for reading in inputs and checking for formatting

def print_map(command):
    var.t_lock.acquire()
    for (host, port), (time, digit) in var.table.items():
        if command=='?':
            msg = "{}:{} --> {}".format(host, port, digit)
            print(msg)
        elif command=='!':
            msg = "{}:{} --> {},{}".format(host, port, time, digit)
            print(msg)
    var.t_lock.release()

def format_input(msg): #returns True if bad input, False if good input
    msg = msg.strip()
    if len(msg)==0:
        return False
    elif len(msg)==1:
        if msg=='q':
            return False
        if msg=='a': #adversial mode
            var.evil = not var.evil
            print('Adversarial mode: {}'.format(var.evil))
            return False
        if msg=='b':
            var.b_lock.acquire()
            print('Blacklist: {}'.format(var.blacklist))
            var.b_lock.release()
            return False
        if msg=='i': #print list of ip with 3 most recent nodes
            var.ip_lock.acquire()
            print('IPs with 3 most recent ports: {}'.format(var.ip))
            var.ip_lock.release()
            return False
        if msg=='?' or msg=='!':
            print_map(msg)
            return False
        else:
            try:
                s = int(msg)
            except:
                return True
            if s>=0 and s<=9:
                addr = '{}:{}'.format(var.HOST, var.PORT)
                t = int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())
                update.update_entry(addr, t, s, mine=True)
                return False

    elif msg[0]=='+':
        i = msg.find(':')
        if i>0:
            host =  msg[1:i]
            port = int(msg[i+1:])
            try:
                host = ipaddress.ip_address(host)
            except:
                return True
            if port>=0 and port<=2**16-1:
                client.connect_node(host, port)
                return False
    
    return True

def read_inputs():
    line = 0
    while line!='q':
        line = input('>>')
        if format_input(line):
            print("Invalid command")