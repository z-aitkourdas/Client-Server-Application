import socket

def Main():
	host = str(input("Enter Server name : "))
	port = 5000

	s = socket.socket()
	s.connect((host,port))

	print('Connected!')
	filename = input('File to download ? => ')
	if filename != '' :
		s.send(bytes(filename,'utf-8'))
		data = s.recv(1024)
		data = data.decode()
		print('data :', data)
		if data[:5] == 'EXIST' :
			filesize = data[5:]
			message = input('File Exists, ' + str(filesize) + \
				                'Bytes, download? (Y/N) -> ')
			if message.lower() == 'y' :
				s.send(bytes('OK', 'utf-8'))
				f = open('Downloaded' + str(filename), 'wb')
				data = s.recv(1024)
				dataRecv = len(data)
				f.write(data)
				while dataRecv < int(filesize) :
					data = s.recv(10000000)
					dataRecv += len(data)
					f.write(data)
					print(dataRecv)
				print ('The file has been completely transfered ')
		else :
			print('File does not Exist!')
	s.close()

if __name__ == '__main__' :
        Main()
