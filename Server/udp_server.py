#!/usr/bin/env python3
"""
    udp_server.py - UDP server that listens on port 9000 and receives and sends back a simple message.
    Author: Matt & Ell
    Date: 3/4/2020
"""
import json
import socket
import time



# Ok so things look different but its the same general idea...
# THE BAD: (TBD)
# Current message logic is not great... this was a temp thing...
# The entire server needs to go to multicast... we should talk about what this means
# If that happens there needs to be some data restructuring ... coolbeans
# and i need to add more comments yeah yeah yeah cool.
class Server:
	UDP_ADDRESS = ""
	UDP_PORT = 0
	session_ips = {}
	known_ips = {}
	sock = None
	current_msg = ""

	def __init__(self, udp_addr, udp_port):
		self.UDP_ADDRESS = udp_addr
		self.UDP_PORT = udp_port
		self.known_ips = self.get_known_ips()
		# create a UDP (DGRAM) socket using tcp-ip (INET)
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


	def send_message(self, msg, addr):
		self.sock.sendto(msg.encode(), addr)


	def get_username(self, addr):
		ip = addr[0]
		if (ip in self.session_ips.keys()):
			return self.session_ips[ip]

		elif(ip in self.known_ips['ips'].keys()):
			return self.known_ips['ips'][ip]

		else:
			self.session_ips[ip] = 'anon'
			return 'anon'

	def change_username(self, addr, new_name):
		ip = addr[0]
		if(ip not in self.session_ips.keys()):
			self.current_msg += "You must already be in the session to change your name. Try saying Hi first."
		else:
			old_name = self.session_ips[ip]
			self.session_ips[ip] = new_name
			self.known_ips['ips'][ip] = new_name
			self.update_known()
			self.current_msg += "Changed name to: {0}".format(new_name)
			print(old_name, " changed their username to ", new_name)

	def get_known_ips(self):
		with open('knownUsers.json') as file:
			ips = json.load(file)
			return ips

	def update_known(self):
		with open('knownUsers.json', 'w') as file:
			json.dump(self.known_ips, file)

	def command(self, data, addr):
		if data[0:12] == "/changename ":
			self.change_username(addr, data[12:50]) # limit lenght of username i guess
		#
		# elif data == "/connect":
		# 	connected_users[addr[0]] = ""
		# 	self.sock.sendto((time.strftime("%H:%M") + " {0} connected".format(addr[0])).encode(), addr)
		#
		# elif data == "/disconnect":
		# 	connected_users.pop(addr[0])
		# 	self.sock.sendto((time.strftime("%H:%M") + " {0} disconnected".format(addr[0])).encode(), addr)
		# 	# print(addr[0] + " disconnected")

		elif data == "/help":
			self.current_msg += "list goes here"

		else:
			# print("invalid command")
			self.current_msg += "Invalid command, for list of commands use '/help'"


	def run(self):
		# bind our socket to the given address/port
		self.sock.bind((self.UDP_ADDRESS, self.UDP_PORT))


		while True:
			data, addr = self.sock.recvfrom(1024)
			data = data.decode()

			# handle commands
			if data[0] == "/":
				self.command(data, addr)

			else:
				username = self.get_username(addr)
				self.current_msg += username + ": " + data
				if(username == 'anon'):
					self.current_msg += "\nHello anon, to change your name enter the command\n/changename <desired name>"
				print(self.current_msg)
			self.send_message(self.current_msg, addr)
			self.current_msg = ""

if __name__ == '__main__':
	server = Server("<YOUR IP HERE>", 9000)
	server.run()
