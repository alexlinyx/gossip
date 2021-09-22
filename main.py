import threading
import server
import client
import controller
import var
import update


#ensure HOST, PORT are set to assigned values
def init_server():
    server.start_server()

def init_client():
    client.start_client()

def init_controller():
    controller.read_inputs()

while True:
    ip = input("Enter address in host:port format. ")
    h,p = update.parse_address(ip)
    if h!='' and p>-1:
        break
var.init_ip(h,p)
#init_server()
#init_client()
init_controller()

#_thread.start_new_thread(init_input, ())
#_thread.start_new_thread(init_server,('127.0.0.1', 1234))
#_thread.start_new_thread(init_client, ())


#thread1(host, port)
#thread2(host, port)

#implement multi threading and locks tomorrow

