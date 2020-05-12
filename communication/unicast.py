import socket
import syslog
import traceback

RECEIVE_BUFF = 1024
ERROR_DATA = '4-True'.encode()


def create_listen_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)
    return sock


def send_config_parameters_player1(connection):
    data = '{}-{}-{}'.format('1', 'O', 'False').encode()
    connection.send(data)


def send_config_parameters_player2(connection):
    data = '{}-{}-{}'.format('1', 'X', 'True').encode()
    connection.send(data)


def server_game_communication(connection1, connection2):
    data = connection2.recv(RECEIVE_BUFF)
    print("Receive data from 2")
    while True:
        try:
            connection1.send(data)
            print("Send data to 1 : " + data.decode())
        except:
            syslog.syslog("Player 1 has closed connection.")
            print("Exception peer close connection")
            connection2.send(ERROR_DATA)
            close_connections(connection1, connection2)
            traceback.print_exc()
            exit(2)

        data = connection1.recv(RECEIVE_BUFF)
        if len(data) == 0:
            syslog.syslog("Player 1 has closed connection.")
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
            syslog.syslog("Player 2 has closed connection.")
            print("Exception peer close connection")
            connection1.send(ERROR_DATA)
            close_connections(connection1, connection2)
            traceback.print_exc()
            exit(4)

        data = connection2.recv(RECEIVE_BUFF)
        if len(data) == 0:
            syslog.syslog("Player 2 has closed connection.")
            print("Exception peer close connection")
            connection1.send(ERROR_DATA)
            close_connections(connection1, connection2)
            traceback.print_exc()
            exit(5)
        print("Receive data from 2 : " + data.decode())


def close_connections(*connections):
    for conn in connections:
        conn.close()
