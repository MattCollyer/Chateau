import socket

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.sendto("/connect".encode(), (MCAST_GRP, MCAST_PORT))

while 1:
    data, addr = sock.recvfrom(10240)
    print(data.decode())

    message = input("Type message and press enter to send.")
    sock.sendto(message.encode(), (MCAST_GRP, MCAST_PORT))

