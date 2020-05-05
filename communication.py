import socket
import struct
import threading
from asyncio import sleep

MCAST_GRP = '224.1.1.1'
BIND_ADDR = '0.0.0.0'
MCAST_PORT = 5007


class Communication:
    stop_thread = False

    def server_multicast_communication(self):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass
        membership = socket.inet_aton(MCAST_GRP) + socket.inet_aton(BIND_ADDR)
        recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
        recv_socket.bind((MCAST_GRP, MCAST_PORT))


        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        while True:
            data = recv_socket.recv(1024)
            if data.decode() == "Searching...":
                send_socket.sendto(b'Hello!', (MCAST_GRP, MCAST_PORT))

    def client_multicast_communication(self):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass
        membership = socket.inet_aton(MCAST_GRP) + socket.inet_aton(BIND_ADDR)
        recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
        recv_socket.bind((MCAST_GRP, MCAST_PORT))

        create_thread(self.client_multicast_search_server())

        while True:
            data = recv_socket.recv(1024)
            if data.decode() == "Hello!":
                host = recv_socket.getpeername()
                print(host)
                self.stop_thread = True
                break
        return host

    def client_multicast_search_server(self):
        while not self.stop_thread:
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            send_socket.sendto(b'Searching...', (MCAST_GRP, MCAST_PORT))
            print("Send packet")
            sleep(5)
        send_socket.close()


def create_thread(target):
    thread = threading.Thread(target=target)
    thread.start()
