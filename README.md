# gossip

Gossip program for CS 6410 at Cornell. Communicate via pull-requests over TCP/IP connections on local network.

Modules are a bit disorganized.
Server handles incoming connections, Client sends outgoing connections, Controller reads user inputs, Update updates the global variables in var.py, main is the entry point of the program.

Command List:
0-9: update own digit
+ipaddress: connect to ipaddress
!: prints map with timestamps
?: prints map
i: prints its with corresponding 3 most updated ports
b: prints blacklisted nodes
a: switch to adversarial mode

python3 main.py to run