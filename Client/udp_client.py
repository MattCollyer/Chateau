#!/usr/bin/env python3
"""
    udp_client.py - UDP client that talks to a remote chat server on UDP port 9000.
    Authors: Matt & Ell
    Date: 4/10/2020

"""

import socket
import sys


class Client:

	UDP_ADDRESS = ''
	UDP_PORT = 0
	sock = None

	def __init__(self, udp_addr = '127.0.0.1', udp_port = 9000):
		self.UDP_ADDRESS = udp_addr
		self.UDP_PORT = udp_port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


	def disconnect(self):
		# Sends a message to the chat server in order to be taken off the list
		print("Disconnected")
		self.sock.sendto("/disconnect".encode(), (self.UDP_ADDRESS, self.UDP_PORT))



	def connect(self):
		# set timeout in case the server doesn't call us back
		self.sock.settimeout(5)
		self.sock.sendto("/connect".encode(), (self.UDP_ADDRESS, self.UDP_PORT))
		print("Type a message and press enter to send! Type /disconnect to quit.")

		while True:
			try:
				data, addr = self.sock.recvfrom(1024)
				print(data.decode())
				message = input()
				if (message == "/disconnect"):
					self.disconnect()
					break
				self.sock.sendto(message.encode(), (self.UDP_ADDRESS, self.UDP_PORT))
			# You can also just control + C ;)
			except KeyboardInterrupt:
				self.disconnect()
				sys.exit()


if __name__ == '__main__':
	client = Client()
	client.connect()
