#!/usr/bin/env python3
"""
    udp_server.py - UDP server that listens on port 9000 and receives and sends back a simple message.
    Author: Matt & Ell
    Date: 3/4/2020
"""
import json
import socket
import time
import threading


# Ok so things look different but its the same general idea...
# THE BAD: (TBD)
# Current message logic is not great... this was a temp thing...
# The entire server needs to go to multicast... we should talk about what this means
# If that happens there needs to be some data restructuring ... coolbeans
# and i need to add more comments yeah yeah yeah cool.
class Server:
    UDP_ADDRESS = ""
    UDP_PORT = 9000
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
        #if known but newly connected, if known but not newly connected, if unknown and newly connected, if unknown and not newly connected
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
        #if (ip not in self.session_ips.keys()): #this should not be necessary anymoe
         #   self.current_msg += "You must already be in the session to change your name. Try saying Hi first."
        #else:
        old_name = self.session_ips[ip]
        self.session_ips[ip] = new_name
        self.known_ips['ips'][ip[0]] = new_name
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
            self.change_username(addr, data[12:50])  # limit lenght of username i guess

        elif data == "/help":
            self.current_msg += "/changename - change display name\n/help - list commands\n/listusers - list currently connected users"

        elif data == "/listusers":
            self.current_msg += str(self.session_ips)

        elif data == "/connect":
            self.current_msg += self.get_username(addr) + " connected"

        elif data == "/disconnect":
            self.current_msg += self.get_username(addr) + " disconnected"
            self.session_ips.pop(addr)

        else:
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
                if (username == 'anon'):
                    self.current_msg += "\nHello anon, to change your name enter the command\n/changename <desired name>"
                print(self.current_msg)
            for ip in self.session_ips:
                self.send_message(self.current_msg, ip) #?
            self.current_msg = ""


if __name__ == '__main__':
    server = Server("127.0.0.1", 9000)  # is there a way/would it be better to get this automatically?
    server.run()