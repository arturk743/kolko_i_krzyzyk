import socket
import threading
import traceback
from threading import Thread
from time import sleep

MCAST_GRP = '224.1.1.1'
BIND_ADDR = '0.0.0.0'
MCAST_PORT = 5007
RECEIVE_BUFF = 1024
ERROR_DATA = '4-True'.encode()


class CommunicationMulticast:
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


class CommunicationUnicast:

    def create_listen_socket(self, host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((host, port))
        sock.listen(100)
        return sock

    def send_config_parameters_player1(self, connection):
        data = '{}-{}-{}'.format('1', 'O', 'False').encode()
        connection.send(data)

    def send_config_parameters_player2(self, connection):
        data = '{}-{}-{}'.format('1', 'X', 'True').encode()
        connection.send(data)

    def server_game_communication(self, connection1, connection2):
        data = connection2.recv(RECEIVE_BUFF)
        print("Receive data from 2")
        while True:
            try:
                connection1.send(data)
                print("Send data to 1 : " + data.decode())
            except:
                print("Exception peer close connection")
                connection2.send(ERROR_DATA)
                close_connections(connection1, connection2)
                traceback.print_exc()
                exit(2)

            data = connection1.recv(RECEIVE_BUFF)
            if len(data) == 0:
                print("Exception peer close connection")
                connection2.send(ERROR_DATA)
                close_connections(connection1, connection2)
                traceback.print_exc()
                exit(3)
            print("Receive data from 1 : " + data.decode())

            try:
                connection2.send(data)
                print("Send data to 2 : " + data.decode())
            except:
                print("Exception peer close connection")
                connection1.send(ERROR_DATA)
                close_connections(connection1, connection2)
                traceback.print_exc()
                exit(4)

            data = connection2.recv(RECEIVE_BUFF)
            if len(data) == 0:
                print("Exception peer close connection")
                connection1.send(ERROR_DATA)
                close_connections(connection1, connection2)
                traceback.print_exc()
                exit(5)
            print("Receive data from 2 : " + data.decode())



def close_connections(*connections):
    for conn in connections:
        conn.close()
