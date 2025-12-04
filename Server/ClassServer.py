import socket
import threading
from pathlib import Path

BUFFER_SIZE = 8192


class Server:
    def __init__(self) -> None:
        self.host_port = 5000
        self.host_name = socket.gethostname()
        self.server_socket = socket.socket()
        self.server_socket.bind((self.host_name, self.host_port))
        self.server_socket.listen(5)

    def start(self) -> None:
        print(f"Server name : {self.host_name}\nPORT : {self.host_port}")
        print("Waiting for Connection ...")

        while True:
            connection, _ = self.server_socket.accept()
            print('Client connect at IP => ' + '<' + str(socket.gethostbyname(self.host_name)) + '>')
            print("Waiting for another Connection ...")
            threading.Thread(target=self.sendFile, args=(connection,), daemon=True).start()

    def listFiles(self, connection: socket.socket) -> None:
        client_response = connection.recv(1024).decode()

        if client_response[:3] == 'YES':
            files_dir = Path.cwd() / "Files"
            for file_name in files_dir.iterdir():
                if file_name.is_file():
                    connection.sendall(f"{file_name.name} ".encode())
            connection.sendall(b"Done")

    def isFile(self, file_name: str):
        path = Path.cwd() / "Files" / file_name
        if path.is_file():
            return 'EXIST' + str(path.stat().st_size)
        return None

    def sendFile(self, connection: socket.socket) -> None:
        try:
            self.listFiles(connection)

            file_to_send = connection.recv(1024).decode()
            file_status = self.isFile(file_to_send)

            if file_status is None:
                connection.sendall(b"File does not exist!")
                return

            connection.sendall(file_status.encode())
            user_response = connection.recv(1024).decode()
            print('Client response : ', user_response[:2])
            if user_response[:2] != 'OK':
                connection.sendall(b'ERR')
                return

            file_path = Path.cwd() / "Files" / file_to_send
            with file_path.open('rb') as f:
                for chunk in iter(lambda: f.read(BUFFER_SIZE), b''):
                    connection.sendall(chunk)
        finally:
            connection.close()


if __name__ == '__main__':
    my_server = Server()
    my_server.start()
