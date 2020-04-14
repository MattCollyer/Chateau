#!/usr/bin/env python3
"""
    udp_client.py - UDP client that talks to a remote server on UDP port 9000 and sends a simple message, and reads
                back what the server sent to it.
    Author: Andrew Cencini (acencini@bennington.edu)
    actually not anymore. update this
    Date: 3/4/2020

"""

import socket
import sys


UDP_ADDRESS = '127.0.0.1'
UDP_PORT = 9000

# first, create the socket - DGRAM == UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# set timeout in case the server doesn't call us back
sock.settimeout(5)

sock.sendto("/connect".encode(), (UDP_ADDRESS, UDP_PORT))

print("Type a message and press enter to send! Type /disconnect to quit.")

while True:
	try:
		data, addr = sock.recvfrom(1024)
		print(data.decode())
		message = input()
		if (message == "/disconnect"):
			print("Disconnected")
			sock.sendto("/disconnect".encode(), (UDP_ADDRESS, UDP_PORT))
			break
		sock.sendto(message.encode(), (UDP_ADDRESS, UDP_PORT))
	except KeyboardInterrupt:
		print("Disconnected")
		sock.sendto("/disconnect".encode(), (UDP_ADDRESS, UDP_PORT))
		sys.exit()


