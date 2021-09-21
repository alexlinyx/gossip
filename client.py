import main
import server
import socket
import random

#sends request every 3 sec to node in map

def connect_node(host, port):
    #set up connection
    try:
        s = socket.create_connection(address=(host,port), timeout=3)
    except TimeoutError:
        main.blacklist.add((host,port))
        del main.table[(host,port)]
        main.ip[host].remove(port)
        return None
    
    data = s.recv().decode(encoding='ascii')
    s.close()
    return data

    

        
        



#connect to port


import socket            
 
# Create a socket object
s = socket.socket()        
 
# Define the port on which you want to connect
port = 12345               
 
# connect to the server on local computer
s.connect(('127.0.0.1', port))
 
# receive data from the server and decoding to get the string.
print (s.recv(1024).decode())
# close the connection
s.close() 