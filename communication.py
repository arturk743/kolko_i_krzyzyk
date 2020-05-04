import socket
import threading
from time import sleep

MCAST_GRP = '224.1.1.1'
MCAST_PORT = 5007


class Communication:
    stop_thread = False

    def server_multicast_communication(self):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass
        recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        recv_socket.bind((MCAST_GRP, MCAST_PORT))
        host = socket.gethostbyname(socket.gethostname())
        recv_socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                               socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)

        while True:
            recv_socket.recv(1024)
            send_socket.sendto(b'Hello!', (MCAST_GRP, MCAST_PORT))

    def client_multicast_communication(self):
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        try:
            recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except AttributeError:
            pass
        recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
        recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

        recv_socket.bind((MCAST_GRP, MCAST_PORT))
        host = socket.gethostbyname(socket.gethostname())
        recv_socket.setsockopt(socket.SOL_IP, socket.IP_ADD_MEMBERSHIP,
                               socket.inet_aton(MCAST_GRP) + socket.inet_aton(host))

        create_thread(self.client__multicast_search_server())

        while True:
            data = recv_socket.recv(1024).decode()
            if data == "Hello!":
                host = recv_socket.getpeername()
                self.stop_thread = True
                break

        return host




    def client__multicast_search_server(self):
        while not self.stop_thread:
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            send_socket.sendto(b'Searching...', (MCAST_GRP, MCAST_PORT))
            print("Send packet")
            sleep(5)

def create_thread(target):
    thread = threading.Thread(target=target)
    thread.daemon = True
    thread.start()

