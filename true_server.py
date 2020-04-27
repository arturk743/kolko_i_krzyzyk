import threading
import socket
from time import sleep

HOST = '127.0.0.1'
PORT = 65432
conn, addr = None, None

running = True
player = "X"
turn = True
playing = 'True'


# create a separate thread to send and receive data from the client


def create_thread(target, connection1, connection2):
    thread = threading.Thread(target=target, args=(connection1, connection2,))
    thread.daemon = True
    thread.start()


# creating a TCP socket for the server


def receive_data(connenction):
    return connenction.recv(1024)  # receive data from the client, it is a blocking method


def send_data(connection, data):
    connection.send(data)


def game_communication(connection1, connection2):
    data = receive_data(connection2)
    print("Receive data from 2")

    while True:
        send_data(connection1, data)
        print("Send data to 1")
        data = receive_data(connection1)
        print("Receive data from 1")

        send_data(connection2, data)
        print("Send data to 2")
        data = receive_data(connection2)
        print("Receive data from 2")


def waiting_for_connection():
    conn1, addr1 = sock.accept()  # wait for a connection, it is a blocking method
    print('client1 is connected')
    send_config_parameters1(conn1)
    conn2, addr1 = sock.accept()  # wait for a connection, it is a blocking method
    print('client2 is connected')
    send_config_parameters2(conn2)
    print('Create thread')
    create_thread(game_communication, conn1, conn2)


def send_config_parameters1(connection):
    data = '{}-{}-{}'.format('1', 'O', 'False').encode()
    send_data(connection, data)


def send_config_parameters2(connection):
    data = '{}-{}-{}'.format('1', 'X', 'True').encode()
    send_data(connection, data)


# run the blocking functions in a separate thread


if __name__ == "__main__":

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(100)

    waiting_for_connection()
    sleep(5000)
    sock.close()