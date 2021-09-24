import threading
import server
import client
import controller
import var
import update
import sys

def init_server(s):
    server.listen_node(s)

def init_client():
    client.start_client()

def init_controller():
    controller.read_inputs()
    sys.exit()


while True:
    ip = input("Enter address in host:port format. ")
    h,p = update.parse_address(ip)
    if h=='' or p==-1:
        print('Invalid ip')
        continue
    try:
        s = server.start_server(p)
    except:
        print('Port in use.')
        continue
    break
var.init_ip(h,p)

#init_server()
#init_client()
#init_controller()


t1 = threading.Thread(target=init_controller)
t2 = threading.Thread(target=init_server, args=(s,), daemon=True)
t3 = threading.Thread(target=init_client, daemon=True)

t1.start()
t2.start()
t3.start()

