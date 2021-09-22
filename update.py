import var
from datetime import datetime
import ipaddress


error = "Invalid command"

def verify_address(host, port):
    try:
        h = ipaddress.ip_address(host)
        p = int(port)
        return p>=0 and p<=2**16-1
    except ValueError:
        return False

def parse_address(addr):
    i = addr.find(':')
    if i>6:
        host = addr[0:i]
        port = addr[i+1:]
        if verify_address(host, port):
            return str(host), int(port)
    print(error)
    return '', -1

def check_old_time(old, new):
    return old<=new

def check_new_time(new):
    t = int((datetime.utcnow()- datetime(1970,1,1)).total_seconds())
    return new<=t

def check_ip(host, port, time):
    try:
        open_ports = var.ip[host]
    except KeyError:
        var.ip[host] = {port}
        return port
    
    if port in open_ports:
        return port
    elif len(open_ports)<3:
        var.ip[host].add(port)
        return port
    else:
        old_time = time
        old_port = port
        for p in open_ports:
            p_time, _ = var.table[host, p]
            if p_time < old_time:
                old_time = p_time
                old_port = p
        if old_port!=port:
            open_ports.add(port)
            open_ports.remove(old_port)
        var.ip[host] = open_ports
        return old_port

### only allow first 3 per ip, check var.ip
# circular import with client!!!!
def update_entry(addr, time, digit):
    host, port = parse_address(addr)
    if (host,port) in var.blacklist:
        return
    
    try:
        last_time, _ = var.table[host, port]
    except KeyError:
        if check_new_time(time):
            #lock
            old_port = check_ip(host, port, time)
            if old_port==port:
                var.table[host,port] = (time, digit)
                msg = "{}:{} --> {}".format(host, port, digit)
                print(msg)
        return
    
    if check_old_time(last_time, time) and check_new_time(time):
        #lock
        old_port = check_ip(host, port, time)
        if old_port==port:
            var.table[host,port] = (time, digit)
            msg = "{}:{} --> {}".format(host, port, digit)
            print(msg)

def update_map(data):
    try:
        lines = data.split(chr(10)) #split on newline, take first 256
    except TypeError:
        print('TypeError')
        return
    if len(lines)>256:
        lines = lines[:256]
    #print(lines)
    for l in lines:
        #print(l)
        try:
            addr, time, digit = l.strip().split(',') #need to check for formatting on inputs
        except ValueError:
            #can I blacklist a node for passing bad information
            #blacklist_node(host, port)
            #return
            continue
        update_entry(addr, int(time), int(digit))
        print(var.table)