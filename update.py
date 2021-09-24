import var
from datetime import datetime
import ipaddress


error = "Invalid command"

def verify_address(host, port):
    try:
        h = ipaddress.ip_address(host)
        p = int(port)
        return p>0 and p<2**16
    except:
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
    var.ip_lock.acquire()
    try:
        open_ports = var.ip[host]
    except:
        var.ip[host] = {port}
        var.ip_lock.release()
        return True
    
    if port in open_ports:
        var.ip_lock.release()
        return True
    elif len(open_ports)<3:
        var.ip[host].add(port)
        var.ip_lock.release()
        return True
    else:
        old_time = time
        old_port = port
        for p in open_ports:
            p_time, _ = var.table[host, p]
            if p_time < old_time:
                old_time = p_time
                old_port = p
        if old_port==port:
            var.ip_lock.release()
            return False
        open_ports.add(port)
        open_ports.remove(old_port)
        del var.table[(host,old_port)]
        var.ip[host] = open_ports
        var.ip_lock.release()
        return True

def check_blacklist(host, port):
    var.b_lock.acquire()
    ret = (host,port) in var.blacklist
    var.b_lock.release()
    return ret

def update_entry(addr, time, digit, mine=False):
    var.t_lock.acquire()
    host, port = parse_address(addr)
    if port==var.PORT and host==var.HOST and not mine: #only I can update my own digit
        var.t_lock.release()
        return
    
    if check_blacklist(host, port):
        var.t_lock.release()
        return
    
    try:
        last_time, last_digit = var.table[host, port]
    except:
        if check_new_time(time):
            if check_ip(host, port, time):
                var.table[host,port] = (time, digit)
                msg = "{}:{} --> {}".format(host, port, digit)
                print(msg)
        var.t_lock.release()
        return
    
    if check_old_time(last_time, time) and check_new_time(time):
        if check_ip(host, port, time):
            var.table[host,port] = (time, digit)
            if last_digit!=digit:
                msg = "{}:{} --> {}".format(host, port, digit)
                print(msg)
    var.t_lock.release()

def update_map(data):
    try:
        lines = data.split(chr(10))
    except:
        return
    if len(lines)>256:
        lines = lines[:256]
    
    for l in lines:
        try:
            addr, time, digit = l.strip().split(',') #need to check for formatting on inputs
        except:
            continue
        try:
            time = int(time)
            digit = int(digit)
        except:
            print('time, digit error')
            continue
        if digit>=0 and digit<=9:
            update_entry(addr, int(time), int(digit))