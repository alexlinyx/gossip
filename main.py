import server
import client

table = {} # host,port: value, timestamp
ip = {} # ip: list of ports, newest to cold
blacklist = {} #set

#implement multi threading and locks tomorrow



def read():
    line = input('>>')
    host, port = format_input(line)

def __init__():
    my_host = '127.0.0.1' #hardcode for now
    my_port = 69 #hardcode for now
    my_digit = 1