import socket

class Client:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port

        self.client_socket = socket.socket()
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print('Connected succefuly!')
        except :
            print("Couldn't connect to the server")
    
    def listFiles(self, cnx):
        list_files = input("Do you want to list all the files in the server? (Y/N) ")
        if list_files.lower() in ['y', 'yes']:
            cnx.send(bytes('YES', 'utf-8'))

            files = cnx.recv(1024)
            print('Data recieved : ', files)
        else:
            cnx.send(bytes("NO", 'utf-8'))
    
    def recvFile(self, cnx):
        file_name = input("Enter the file you want to download with the extention -> ")

        if file_name != '':
            cnx.send(bytes(file_name, 'utf-8'))

            server_response = cnx.recv(1024)
            server_response = server_response.decode()

            if server_response[:5] == 'EXIST':
                file_size = server_response[5:]
                msg = input("File Exists, "+str(file_size)+'Mb, download? (Y/N) -> ')
                
                if msg.lower() in ['y', 'yes'] :
                    cnx.send(bytes('OK', 'utf-8'))
                    
                    try:
                        f = open(file_name, 'wb')
                        data_recv = 0

                        while data_recv < file_size:
                            data = cnx.recv(10_000_000)
                            data_recv += len(data)
                            f.write(data)
                        print("The file has been comppletely transferd!")
                    except :
                        print("An exception occurred!")
                    finally:
                        f.close()
            else :
                srv_response = cnx.recv(1024).decode()
                print(srv_response)

    def start(self):
        self.listFiles(self.client_socket)
        self.recvFile(self.client_socket)
        self.client_socket.close()

if __name__ == '__main__':
    server_host = input("Enter the server host name : ")
    server_port = int(input("Enter the server port : "))
    client = Client(server_host, server_port)
    client.start()