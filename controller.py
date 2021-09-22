import ipaddress
from datetime import datetime
import var
import client
import update

#for reading in inputs and checking for formatting


error = "Invalid command"

def print_map(command):
    msg = error
    for (host, port), (time, digit) in var.table.items():
        if command=='?':
            msg = "{}:{} --> {}".format(host, port, digit)
        elif command=='!':
            msg = "{}:{} --> {},{}".format(host, port, time, digit)
        print(msg)

def format_input(msg):
    msg = msg.strip()
    if len(msg)==0:
        pass

    elif len(msg)==1:
        if msg=='q':
            return
        if msg=='?' or msg=='!':
            print_map(msg)
            return
        else:
            try:
                s = int(msg)
            except ValueError:
                print(error)
                return
            if s>=0 and s<=9:
                addr = '{}:{}'.format(var.HOST, var.PORT)
                t = int((datetime.utcnow()-datetime(1970,1,1)).total_seconds())
                update.update_entry(addr, t, s)
                return

    elif msg[0]=='+':
        i = msg.find(':')
        if i>0:
            host =  msg[1:i]
            port = int(msg[i+1:])
            try:
                host = ipaddress.ip_address(host)
            except ValueError:
                print(error)
                return
            if port>=0 and port<=2**16-1:
                client.connect_node(host, port)
                print('Connection Sucessful')
                return
    
    print(error)

def read_inputs():
    line = 0
    while line!='q':
        line = input('>>')
        format_input(line)