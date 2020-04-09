#!/usr/bin/env python3
"""
    udp_client.py - UDP client that talks to a remote server on UDP port 9000 and sends a simple message, and reads
                back what the server sent to it.
    Author: Andrew Cencini (acencini@bennington.edu)
    Date: 3/4/2020
"""

import socket


UDP_ADDRESS = "<YOUR IP HERE>"
UDP_PORT = 9000

# first, create the socket - DGRAM == UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set timeout in case the server doesn't call us back
sock.settimeout(5)

print("Type a message and press enter to send!")
while True:
	message = input()
	sock.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
	data, addr = sock.recvfrom(1024)
	print(data.decode())
