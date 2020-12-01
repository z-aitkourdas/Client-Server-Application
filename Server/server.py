import socket
import os
import threading


def RecvFile(name, sock):
        filename = sock.recv(1024)
        filename = filename.decode()
        # print(filename)
        if os.path.isfile(str(filename)):
                sock.send(bytes('EXIST' + str(os.path.getsize(filename)),'utf-8'))
                userResponse = sock.recv(1024)
                userResponse = userResponse.decode()
                print('Client response : ',userResponse[:2])
                if userResponse[:2] == 'OK' :
                        with open(filename, 'rb') as f :
                                bytesToSend = f.read(1024)
                                sock.send(bytesToSend)
                                while bytesToSend != '' :
                                        bytesToSend = f.read(100000000)
                                        sock.send(bytesToSend)
        else :
                sock.send(bytes('ERR', 'utf-8'))
        sock.close()
	

def Main():
        host = socket.gethostname()
        port = 5000
        s = socket.socket()
        s.bind((host,port))
        s.listen(5)
        print ("Server name : ",host)
        while True :
                print("Waiting for Connection ...")
                cnx, addr = s.accept()
                print('Client connect at IP => ' + '<' + str(socket.gethostbyname(host)) + '>')
                t = threading.Thread(target=RecvFile, args=('recvThread', cnx))
                t.start()
        s.close()

if __name__ == '__main__':
        Main()
