#!/usr/bin/env python3
"""
    udp_server.py - UDP server that listens on port 9000 and receives and sends back a simple message.
    Author: Matt & Ell
    Date: 4/10/2020
"""
import json
import socket

# UDP Server, default udp addr is localhost, port 9000.
class Server:
    UDP_ADDRESS = ""
    UDP_PORT = 0
    session_ips = {}
    known_ips = {}
    sock = None
    unique_msg = ""
    serverwide_msg = ""

    def __init__(self, udp_addr = "127.0.0.1", udp_port = 9000):
        self.UDP_ADDRESS = udp_addr
        self.UDP_PORT = udp_port
        self.known_ips = self.get_known_ips()
        # create a UDP (DGRAM) socket using tcp-ip (INET)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, msg, addr):
        self.sock.sendto(msg.encode(), addr)

	# Sends message to all users in session,
	# some messages are unique ( from the server to one user )
    def send_to_users(self, recent_address):
        for address in self.session_ips:
            message = self.serverwide_msg
            if (address == recent_address):
                message = self.unique_msg + "\n" + self.serverwide_msg
            self.send_message(message, address)

    def get_username(self, addr):
        #if known but newly connected,
        #if known but not newly connected,
        #if unknown and newly connected, if unknown and not newly connected
        if (addr not in self.session_ips) & (addr[0] in self.known_ips['ips']):
            self.session_ips[addr] = self.known_ips['ips'][addr[0]]
            return self.session_ips[addr]

        elif (addr[0] in self.known_ips['ips']):
            return self.session_ips[addr]

        elif (addr not in self.session_ips):
           self.session_ips[addr] = "anon"
           return ('anon ' + "(" +addr[0]+ ")")

        else:
            return ('anon ' + "(" + addr[0] + ")")

    def change_username(self, addr, new_name):
        ip = addr
        old_name = self.session_ips[ip]
        self.session_ips[ip] = new_name
        self.known_ips['ips'][ip[0]] = new_name
        self.update_known()
        self.serverwide_msg += "{0} changed their name to {1}".format(old_name, new_name)

    #loads in a json of previously logged addresses and usernames
    def get_known_ips(self):
        with open('knownUsers.json') as file:
            ips = json.load(file)
            return ips

    # Updates said file
    def update_known(self):
        with open('knownUsers.json', 'w') as file:
            json.dump(self.known_ips, file)


    def command(self, data, addr):
        if data[0:12] == "/changename ":
            self.change_username(addr, data[12:50])  # limit lenght of username i guess

        elif data == "/help":
            self.unique_msg += "/changename - change display name\n/help - list commands\n/listusers - list currently connected users"

        elif data == "/listusers":
            self.unique_msg += str(self.session_ips)

        elif data == "/connect":
            self.serverwide_msg += self.get_username(addr) + " connected"

        elif data == "/disconnect":
            self.serverwide_msg += self.get_username(addr) + " disconnected"
            self.session_ips.pop(addr)

        else:
            self.unique_msg += "Invalid command, for list of commands use '/help'"


    def run(self):
        # bind our socket to the given address/port
        self.sock.bind((self.UDP_ADDRESS, self.UDP_PORT))

        while True:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode()

            # handle commands
            if data[0] == "/":
                self.command(data, addr)
            # if normal message, grab username
            else:
                username = self.get_username(addr)
                self.serverwide_msg += username + ": " + data
                if (username == 'anon'):
                    self.unique_msg += "\nHello anon, to change your name enter the command\n/changename <desired name>"
            # Send to all :)
            self.send_to_users(addr)
            self.unique_msg = ""
            self.serverwide_msg = ""


if __name__ == '__main__':
    server = Server()
    server.run()
