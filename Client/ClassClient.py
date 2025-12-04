import socket
from pathlib import Path

BUFFER_SIZE = 8192


class Client:
    def __init__(self, server_host: str, server_port: int):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket()

        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print('Connected successfully!')
        except OSError:
            print("Couldn't connect to the server")
            self.client_socket = None

    def listFiles(self, cnx: socket.socket) -> None:
        list_files = input("Do you want to list all the files in the server? (Y/N) ")
        if list_files.lower() in ['y', 'yes']:
            cnx.sendall(b'YES')

            file_rcv = cnx.recv(BUFFER_SIZE).decode()
            while file_rcv.split()[-1] != 'Done':
                file_rcv += cnx.recv(BUFFER_SIZE).decode()
            print(file_rcv[:-5])
        else:
            cnx.sendall(b"NO")

    def _download(self, cnx: socket.socket, file_name: str, file_size: int) -> None:
        destination = Path.cwd() / 'Downloads'
        destination.mkdir(exist_ok=True)
        full_path = destination / file_name

        if full_path.is_file() and full_path.stat().st_size == file_size:
            print("The file already exists!")
            return

        with full_path.open('wb') as f:
            data_recv = 0
            while data_recv < file_size:
                data = cnx.recv(BUFFER_SIZE)
                if not data:
                    break
                data_recv += len(data)
                f.write(data)
        print("The file has been completely transferred!")

    def recvFile(self, cnx: socket.socket) -> None:
        file_name = input("Enter the file you want to download with the extension -> ")

        if file_name:
            cnx.sendall(file_name.encode())

            server_response = cnx.recv(BUFFER_SIZE).decode()

            if server_response[:5] == 'EXIST':
                file_size = float(server_response[5:])
                if file_size // 10**3 == 0:
                    msg = input(f"File Exists, {file_size}Bytes, download? (Y/N) -> ")
                elif file_size // 10**3 >= 1 and file_size // 10**3 < 10**3:
                    msg = input(f"File Exists, {file_size/10**3}KB, download? (Y/N) -> ")
                elif file_size // 10**6 >= 1:
                    msg = input(f"File Exists, {file_size//10**6}MB, download? (Y/N) -> ")
                else:
                    msg = input(f"File Exists, {file_size}Bytes, download? (Y/N) -> ")

                if msg.lower() in ['y', 'yes']:
                    cnx.sendall(b'OK')
                    self._download(cnx, file_name, int(file_size))
            else:
                print(server_response)

    def start(self) -> None:
        if not self.client_socket:
            return
        self.listFiles(self.client_socket)
        self.recvFile(self.client_socket)
        self.client_socket.close()


if __name__ == '__main__':
    server_host = input("Enter the server host name : ")
    server_port = int(input("Enter the server port : "))
    client = Client(server_host, server_port)
    client.start()
