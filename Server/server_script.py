#!/usr/bin/env python3
""" Python script to handle the server side."""
import socket
import os
import sys
import threading  # For multi-threading


def list_files(connection):
    """ This methode lists all the files available in the server """

    client_response = connection.recv(1024)  # Get the client request
    client_response = client_response.decode()  # Decode the request

    # Check if the client wants to list all the files or not
    if client_response[:3] == 'YES':

        # If it's the case we are going to send file names located in the server
        for file_name in os.listdir(os.getcwd() + "\\Files"):
            connection.send(bytes(file_name + '\t', 'utf-8'))
        connection.send(bytes("Done", "utf-8"))

    return 0


class Server:
    """ Create a server class to handle multiple users requests """
    def __init__(self):
        # Initiate the server port
        self.host_port = 5050
        self.host_name = socket.gethostname()
        self.server_ip = socket.gethostbyname(self.host_name)  # You can use a different IP address.

        # Create a socket object
        self.server_socket = socket.socket()
        # Bind the socket to the local address
        try:
            self.server_socket.bind(('', self.host_port))
        except socket.error as msg:
            print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
            sys.exit()

        self.server_socket.listen(5)

    def start(self):
        """ Start the server. """
        print("Server name : {}\nIP: {}\nPORT : {}"
              .format(self.host_name, self.server_ip, self.host_port))
        print("Waiting for Connection ...")

        while True:
            cnn, addr = self.server_socket.accept()
            print('\nA client connected to the server at @ ' + '<' + str(addr) + '>', end='\n\n')

            # print("Waiting for another Connection ...")

            thread = threading.Thread(target=self.send_file, args=(cnn, ))
            thread.start()
        # self.server_socket.close()

    def is_file(self, file_name):
        """ This methode check whether the given file name is valid or not """

        if file_name != '':
            print(f"The client at @ {socket.gethostbyname(self.host_name)} "
                  f"wants to download '{file_name}' file.")
            path = os.getcwd() + "\\Files\\"
            if os.path.isfile(path + file_name):
                return 'EXIST' + str(os.path.getsize(path + file_name))
            # There is no such file with the name given.
            return None

        # No file name is given.
        return None

    def send_file(self, connection):
        """ This methode handles file transfer to the client """

        list_files(connection)

        file_to_send = connection.recv(1024)  # Get the file name
        file_to_send = file_to_send.decode()

        is_file = self.is_file(file_to_send)  # Check if it's a valid file name

        # If it's the case we are going to send the file
        if is_file is not None:
            # Send a message to tell the client that the chosen file exist in the server
            connection.send(bytes(is_file, 'utf-8'))

            user_response = connection.recv(1024)
            user_response = user_response.decode()

            # print('Client response : ',user_response[:2])
            if user_response[:2] == 'OK':
                with open(os.getcwd() + "\\Files\\" + file_to_send, 'rb') as file:
                    print("Sending the file ...")
                    bytes_to_send = file.read()
                    connection.send(bytes_to_send)

                    print(f"The {file_to_send} has been sent to the client.")

                    # while bytes_to_send != b'':
                    #     bytes_to_send = file.read()
                    #     connection.send(bytes_to_send)
            else:
                connection.send(bytes('ERR', 'utf-8'))

        else:
            connection.send(bytes("File does not exist!", 'utf-8'))

        # connection.close()


if __name__ == '__main__':
    my_server = Server()
    my_server.start()
