import socket
import os
import threading

def fileList(sock):
        for file_name in os.listdir(os.getcwd()):
                sock.send(bytes(file_name), 'utf-8')

def RecvFile(name, sock):
        # Getting the filename meant to be downloaded
        filename = sock.recv(1024)
        filename = filename.decode()

        if os.path.isfile(str(filename)):  # Checking if it's a file and exist or not
                # Sending a message to let the client know if the file exist or not
                sock.send(bytes('EXIST' + str(os.path.getsize(filename)),'utf-8'))
                
                # Get the client response (if he want to download the file or not)
                userResponse = sock.recv(1024)
                userResponse = userResponse.decode()

                print('Client response : ',userResponse[:2])
                if userResponse[:2] == 'OK' :
                        with open(filename, 'rb') as f :
                                # Process the file to send it
                                bytesToSend = f.read(1024)
                                sock.send(bytesToSend)
                                while bytesToSend != '' :
                                        bytesToSend = f.read(100000000)
                                        sock.send(bytesToSend)
        else :
                # Send an eror message because the file doesn't exist
                sock.send(bytes('ERR', 'utf-8'))
        sock.close()



def Main():
        host = socket.gethostname()  # Get the server name
        port = 5000  # Set the default port for the server
        
        s = socket.socket()  # Creating a socket object
        s.bind((host,port))  # Bind the socket to the local address

        s.listen(5)  # Accept 5 connection

        print ("Server name : {} \t at PORT : {}".format(host, port))
        print("Waiting for Connection ...")
        while True :
                cnx, addr = s.accept()  # Accept the incoming connection
                print('Client connect at IP => ' + '<' + str(socket.gethostbyname(host)) + '>')
                
                print("Waiting for another Connection ...")
                # Managing multiple connections
                t = threading.Thread(target=RecvFile, args=('recvThread', cnx))
                t.start()
        
        s.close()  # Close the socket

if __name__ == '__main__':
        Main()
