import socket
import os
import threading

class Server:
    def __init__(self):
        self.host_port = 5000
        self.host_name = socket.gethostname()

        self.server_socket = socket.socket()
        self.server_socket.bind((self.host_name, self.host_port))

        self.server_socket.listen(5)
    
    def start(self):
        print ("Server name : {}\n PORT : {}".format(self.host_name, self.host_port))
        print("Waiting for Connection ...")

        while True:
            self.cnn, addr = self.server_socket.accept()
            print('Client connect at IP => ' + '<' + str(socket.gethostbyname(self.host_name)) + '>')

            print("Waiting for another Connection ...")

            t = threading.Thread(target=self.sendFile, args=('recvThread',self.cnn))
            t.start()
        self.server_socket.close()

    def listFiles(self, connection):
        client_response = connection.recv(1024)
        client_response = client_response.decode()

        if client_response[:3] == 'YES':
            for file_name in os.listdir(os.getcwd()):
                connection.send(bytes(file_name, 'utf-8'))
    
    def isFile(self, file_name):
        if os.path.isfile(file_name):
            return 'EXIST' + str(os.path.getsize(file_name)/1024)
        else:
            return None
 
    def sendFile(self, name, connection):
        file_to_send = connection.recv(1024)
        file_to_send = file_to_send.decode()

        self.listFiles(connection)

        is_file = self.isFile(file_to_send)

        if is_file != None:
            cofile_to_send = connection.send(bytes(is_file, 'utf-8'))

            user_response = cofile_to_send = connection.recv(1024)
            user_response = user_response.decode()

            print('Client response : ',user_response[:2])
            if user_response[:2] == 'OK':
                with open(file_to_send, 'rb') as f:
                    bytes_to_send = f.read(file_to_send)
                    cofile_to_send = connection.send(bytes_to_send)

                    while bytes_to_send != '':
                        bytes_to_send = f.read(100000000)
                        cofile_to_send = connection.send(bytes_to_send)
            else:
                cofile_to_send = connection.send(bytes('ERR', 'utf-8'))
            cofile_to_send = connection.close()

if __name__ == '__main__' :
    my_server = Server()
    my_server.start()