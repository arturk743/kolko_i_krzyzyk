import socket
import traceback
import syslog

class ServerCommunication:

    def create_socket(self, host, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(100)
            return sock
        except Exception as ex:
            syslog.syslog(syslog.LOG_ERR,
                          "failed to socekt (%s)" %
                          str(ex))

    def receive_data(self, connection):
        try:
            data = connection.recv(1024)  # receive data from the client, it is a blocking method
            return data
        except Exception as ex:
            syslog.syslog(syslog.LOG_ERR,
                          "failed to receive data archives request event (%s)" %
                          str(ex))

    def send_data(self, connection, data):
        try:
            connection.send(data)
        except Exception as ex:
            syslog.syslog(syslog.LOG_ERR,
                          "failed to send data archives request event (%s)" %
                          str(ex))

    def send_config_parameters_player1(self, connection):
        data = '{}-{}-{}'.format('1', 'O', 'False').encode()
        self.send_data(connection, data)

    def send_config_parameters_player2(self, connection):
        data = '{}-{}-{}'.format('1', 'X', 'True').encode()
        self.send_data(connection, data)

    def game_communication(self, connection1, connection2):
        data = self.receive_data(connection2)
        print("Receive data from 2")
        while True:
            try:
                self.send_data(connection1, data)
                print("Send data to 1 : " + data.decode())
            except:
                traceback.print_exc()
                exit(2)

            try:
                data = self.receive_data(connection1)
                if len(data) == 0:
                    print("Exception peer close connection")
                    exit(4)
                print("Receive data from 1 : " + data.decode())
            except:
                traceback.print_exc()
                exit(3)
            try:
                self.send_data(connection2, data)
                print("Send data to 2 : " + data.decode())
            except:
                traceback.print_exc()
                exit(4)
            try:
                data = self.receive_data(connection2)
                if len(data) == 0:
                    print("Exception peer close connection")
                    exit(4)
                print("Receive data from 2 : " + data.decode())
            except:
                traceback.print_exc()
                exit(5)