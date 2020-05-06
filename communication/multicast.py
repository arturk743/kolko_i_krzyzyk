import socket
import threading
from time import sleep

MCAST_GRP = '224.1.1.1'
BIND_ADDR = '0.0.0.0'
MCAST_PORT = 5007
RECEIVE_BUFF = 1024

class Multicast:
    stop_thread = False

    def server_communication(self):
        recv_socket = create_receive_socket()
        send_socket = create_send_socket()

        while True:
            data = recv_socket.recv(RECEIVE_BUFF)
            if data.decode() == "Searching...":
                send_socket.sendto(b'Hello!', (MCAST_GRP, MCAST_PORT))

    def client_communication(self):
        recv_socket = create_receive_socket()
        thread = create_thread(self.__client_search_server)

        while True:
            print("Waiting")
            data, addr = recv_socket.recvfrom(RECEIVE_BUFF)
            if data.decode() == "Hello!":
                self.stop_thread = True
                print("Success")
                break
        thread.join()
        recv_socket.close()
        return addr[0]

    def __client_search_server(self):
        while not self.stop_thread:
            send_socket = create_send_socket()
            send_socket.sendto(b'Searching...', (MCAST_GRP, MCAST_PORT))
            print("Send packet")
            sleep(2)
        send_socket.close()


def create_receive_socket():
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        recv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except AttributeError:
        pass
    membership = socket.inet_aton(MCAST_GRP) + socket.inet_aton(BIND_ADDR)
    recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)
    recv_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    recv_socket.bind((MCAST_GRP, MCAST_PORT))
    return recv_socket


def create_send_socket():
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 0)
    return send_socket


def create_thread(target):
    thread = threading.Thread(target=target, args=())
    thread.daemon = True
    thread.start()
    return thread

