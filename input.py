import ipaddress
import socket
import threading
import time
from datetime import datetime
import main
import client

table = {} # host,port: value, timestamp
ips = {} # ip: list of ports, newest to cold

#placeholders for ? abnd ! commands
question = 0
exclaim = 0
error = "Invalid command"

def verify(host, port):
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    if port>=0 and port<=2**16-1:
        return True
    return False

def parse_address(addr):
    i = addr.find(':')
    if i>6:
        host = addr[0:i]
        port = int(addr[i+1])
        if verify(host, port):
            return host, port
    print(error)
    return '', -1

def combine_address(host, port):
    if verify(host,port):
        return host + ':' + str(port)
    print(error)
    return ''

def check_old_time(old, new):
    return old<new

def check_new_time(new):
    t = int((datetime.utcnow()- datetime(1970,1,1)).total_seconds())
    return new<t

def update_entry(addr, digit, time):
    host, port = parse_address(addr)
    if host=='':
        return
    try:
        last_digit, last_time = table[host, port]
    except TypeError:
        if check_new_time(time):
            table[host,port] = (digit, time)
    if check_old_time(last_time, time) and check_new_time(time):
        #lock
        table[host,port] = (digit, time)



def format_input(msg):
    msg = msg.trim()
    if len(msg)==0:
        pass

    elif len(msg)==1:
        if msg=='?':
            print(question)
        elif msg=='!':
            print(exclaim)
        else:
            s = int(msg)
            if s>=0 and s<=9:
                my_digit = s

    elif msg[0]=='+':
        i = msg.find(':')
        if i>0:
            host =  msg[1:i]
            port = int(msg[i+1])
            try:
                ip = ipaddress.ip_address(host)
            except ValueError:
                print(error)
                return '',-1
            if port>=0 and port<=2**16-1:
                return ip, port
    
    print(error)
    return '',-1

def read():
    line = input('>>')
    host, port = format_input(line)