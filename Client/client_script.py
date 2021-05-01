#!/usr/bin/ env python3
""" Python script to handle the clients side."""
import socket
import os
import time
from sys import exc_info, platform


def format_file_size(size):
    """
    Formatted size of the file on Bytes, KB, MB or GB.
    :param size: the size of the file in Bytes.
    :return: Formatted size of the file on Bytes, KB, MB or GB.
    """
    output_msg = "File Exists "
    if size // 10 ** 3 <= 0:
        output_msg += str(size) + "Bytes."
    elif (size // (10 ** 3)) < 10 ** 3:
        output_msg += str(size / 10 ** 3) + "KB. "
    elif size // 10 ** 6 >= 1:
        output_msg += str(size // 10 ** 6) + "MB. "
    elif size // 10 ** 9 >= 1:
        output_msg += str(size // 10 ** 9) + "GB. "
    output_msg += "Do you want to download it? (Y/N) -> "
    return output_msg


def format_time(number_seconds):
    """
    Format the given time in seconds into minutes or hours.
    :param number_seconds: The time on seconds.
    :return: Formatted time.
    """
    if number_seconds // 60 == 0:
        output_msg = "{:.4f}s".format(number_seconds)
    elif number_seconds // 60 >= 1 and number_seconds < 60:
        output_msg = "{}min{:.4f}s".format(number_seconds // 60, number_seconds % 60)
    else:
        output_msg = "{}h{}min{:.4f}s" \
            .format(number_seconds // 3600, number_seconds // 60, number_seconds % 60)

    print(f"\nThe file has been completely transferred! in {output_msg}")


def handle_download(cnx, file_name, file_size):
    """
    Download the given file from the server.
    :param cnx: A socket object.
    :param file_name: The desire file name.
    :param file_size: The size of the file.
    :return: Download the file and put it in the Downloads folders.
    """
    # Try to create a folder for the download
    full_path = ""
    if platform == "win32":
        try:
            full_path = os.getcwd() + "\\Downloads\\" + file_name
            os.makedirs('Downloads', exist_ok=True)

        except exc_info()[0]:
            print("\nOops!", exc_info()[0], " occurred!")

    try:
        full_path = os.getcwd() + "/Downloads/" + file_name
        os.makedirs('Downloads', exist_ok=True)

    except exc_info()[0]:
        print("\nOops!", exc_info()[0], " occurred!")

    # Check if the file already exist
    if os.path.isfile(full_path) and os.path.getsize(full_path) == file_size:
        print("\nThe file already exist!")

    else:
        file = open(full_path, 'wb')
        data_recv = 0

        start = time.time()
        while data_recv < file_size:
            data = cnx.recv(10 ** 8)
            data_recv += len(data)
            file.write(data)
        end = time.time()
        file.close()

        download_time = end - start
        format_time(download_time)
    # finally:
    #     f.close()


def recv_file(cnx):
    """
     Receives the file from the server.
    :param cnx: A socket object connected to the server.
    :return: Download the file from the server.
    """

    # Get the name of the file the client wants
    file_name = input("\nEnter the file you want to download with the extension -> ")

    # If the client provide a name we start to retrieve the file from the server
    if file_name != '':
        cnx.send(bytes(file_name, 'utf-8'))  # Sent the file name to the server

        server_response = cnx.recv(1024)  # Retrieve the server response
        server_response = server_response.decode()  # Decode it

        # Check if the file exist or not
        if server_response[:5] == 'EXIST':
            file_size = float(server_response[5:])  # Get the size of the file

            # Show the size on Bytes, KB, MB or GB
            size_ = format_file_size(file_size)
            client_response = input(size_)

            # Check if the client wants to proceed the download
            if client_response.lower() in ['y', 'yes']:
                cnx.send(bytes('OK', 'utf-8'))  # Send the request to the server

                handle_download(cnx, file_name=file_name, file_size=file_size)
        else:
            print(server_response)
    else:
        print("\nYou did not choose any file !!!")


def list_files(cnx):
    """ Send a request to either lists all the files available in the server or not """
    # Get the client answer
    show_files = input("Do you want to list all the files in the server? (Y/N) ")
    # Check if the client wants to list all the files
    if show_files.lower() in ['y', 'yes']:
        cnx.send(bytes('YES', 'utf-8'))  # If that's the case we send a request to the server

        # Receiving all the files from the server
        file_rcv = cnx.recv(1024).decode()
        while file_rcv.split()[-1] != 'Done':
            file_rcv += cnx.recv(1024).decode()
        print(file_rcv[:-5])
    else:
        cnx.send(bytes("NO", 'utf-8'))


class Client:
    """ Create a client class to handle multiple users and send all the requests"""

    def __init__(self, host, port):
        self.server_host = host  # The server host name
        self.server_port = port  # The server port

        self.client_socket = socket.socket()  # Create a socket object for the client
        # Try to connect with the server
        print('\nTrying to connect to the server ...')
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print('Connected successfully!', end='\n\n')
            self.flag = True
        except InterruptedError:
            print("Couldn't connect to the server", end='\n\n')
            self.flag = False

    def start(self):
        """ This methode start the hole process of listing and retrieving the file """

        if self.flag:
            list_files(self.client_socket)
            recv_file(self.client_socket)
            self.client_socket.close()


if __name__ == '__main__':
    server_host = input("Enter the server host name : ")
    server_port = int(input("Enter the server port : "))

    STILL_DOWNLOAD = 'yes'
    while STILL_DOWNLOAD.lower() in ('y', 'yes'):
        client = Client(server_host, server_port)  # Create a client object
        client.start()
        STILL_DOWNLOAD = input('Do you want to download another file (Y/N)? ')
