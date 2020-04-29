import threading
from server_communication import ServerCommunication

HOST = '127.0.0.1'
PORT = 65432


class Server:

    def __init__(self):
        self.server_communication = ServerCommunication()
        self.sock = self.server_communication.create_socket(HOST, PORT)
        while True:
            self.waiting_for_connection()
        self.sock.close()

    def waiting_for_connection(self):
        conn1, addr1 = self.sock.accept()  # wait for a connection, it is a blocking method
        print('client1 is connected')
        self.server_communication.send_config_parameters_player1(conn1)
        conn2, addr1 = self.sock.accept()  # wait for a connection, it is a blocking method
        print('client2 is connected')
        self.server_communication.send_config_parameters_player2(conn2)
        print('Creating thread')
        create_thread(self.server_communication.game_communication, conn1, conn2)


def create_thread(target, connection1, connection2):
    thread = threading.Thread(target=target, args=(connection1, connection2,))
    thread.daemon = True
    thread.start()


if __name__ == "__main__":
    server = Server()
