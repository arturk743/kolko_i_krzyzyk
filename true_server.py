import syslog
import threading
from communication.multicast import Multicast
import communication.unicast as ucast_communication

HOST = '0.0.0.0'
PORT = 5008


class Server:

    def __init__(self):
        create_thread2(Multicast().server_communication)
        self.sock = ucast_communication.create_listen_socket(HOST, PORT)
        while True:
            self.waiting_for_connection()
        self.sock.close()

    def waiting_for_connection(self):
        conn1, addr1 = self.sock.accept()  # wait for a connection, it is a blocking method
        print('client1 is connected')
        ucast_communication.send_config_parameters_player1(conn1)
        conn2, addr1 = self.sock.accept()  # wait for a connection, it is a blocking method
        print('client2 is connected')
        ucast_communication.send_config_parameters_player2(conn2)
        print('Creating thread')
        create_thread(ucast_communication.server_game_communication, conn1, conn2)


def create_thread(target, connection1, connection2):
    try:
        thread = threading.Thread(target=target, args=(connection1, connection2,))
        thread.daemon = True
        thread.start()

    except Exception as ex:
        syslog.syslog(syslog.LOG_ERR,
                      "Error creating thread")


def create_thread2(target):
    thread = threading.Thread(target=target, args=())
    thread.daemon = True
    thread.start()
""" sprobowac polaczyc dwa create_thread
def create_thread(target, *arguments):
    try:
        thread = threading.Thread(target=target, args=(*arguments))
        thread.daemon = True
        thread.start()

    except Exception as ex:
        syslog.syslog(syslog.LOG_ERR,
                      "Error creating thread")

"""
if __name__ == "__main__":
    server = Server()
