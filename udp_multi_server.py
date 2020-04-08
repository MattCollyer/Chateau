import socket
import struct
import time

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

connected_users = {}

sock.bind(('', MCAST_PORT))

mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while 1:
    data, addr = sock.recvfrom(1024)
    data = data.decode()

    # handle commands
    if data[0] == "/":
        if data[0:9] == "/setname ":
            connected_users[addr[0]] = data[9:50] # limit lenght of username i guess
            sock.sendto((time.strftime("%H:%M") + " {0} changed name to ".format(addr[0]) + connected_users[addr[0]]).encode(), addr)
            # print(addr[0] + " changed name to " + connected_users[addr[0]])

        elif data == "/connect":
            connected_users[addr[0]] = ""
            sock.sendto((time.strftime("%H:%M") + " {0} connected".format(addr[0])).encode(), addr)

        elif data == "/disconnect":
            connected_users.pop(addr[0])
            sock.sendto((time.strftime("%H:%M") + " {0} disconnected".format(addr[0])).encode(), addr)
            # print(addr[0] + " disconnected")

        elif data == "/help":
            sock.sendto("list goes here".encode(), addr)

        else:
            # print("invalid command")
            sock.sendto("Invalid command, for list of commands use '/help'".encode(), addr)

    else:
        username = connected_users[addr[0]]
        if username == "":
            sock.sendto((time.strftime("%H:%M") + " {0}: {1}".format(addr[0], data)).encode(), addr)
            # print(time.strftime("%H:%M") + " {0}: {1}".format(addr[0], data))
        else:
            sock.sendto((time.strftime("%H:%M") + " {0}: {1}".format(username,
                                                               data)).encode(), addr)
            # print(time.strftime("%H:%M") + " {0}: {1}".format(username,
                                                              # data))