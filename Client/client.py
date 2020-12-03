import socket

def Main():
	host = str(input("Enter Server name : "))
	port = 5000

	# Create a socket object
	s = socket.socket()
	s.connect((host,port))  # Connect to the server

	print('Connected!')
	filename = input('File to download ? => ')  # File to download
	if filename != '' :
		# Sending the request
		s.send(bytes(filename,'utf-8'))
		
		# Getting the response from the server
		data = s.recv(1024)
		data = data.decode()

		if data[:5] == 'EXIST' :  # Check if the file exist or not
			# Get the file size from the response
			filesize = data[5:]
			message = input('File Exists, ' + str(filesize) + 'Bytes, download? (Y/N) -> ')

			if message.lower() in ['y', 'yes'] :  # Check if the client want to continue the download
				s.send(bytes('OK', 'utf-8'))  # To let the server that we want to dowanload the file
				
				f = open('Downloaded_' + str(filename), 'wb')  # Create the file that we want
				
				# Recieve the data from the server
				data = s.recv(1024)
				dataRecv = len(data)
				f.write(data)  # Write the recieved data
				while dataRecv < int(filesize) :
					data = s.recv(10000000)
					dataRecv += len(data)
					f.write(data)
					print(dataRecv)
				f.close()
				print ('The file has been completely transfered ')
		else :
			print('File does not Exist!')
	s.close()

if __name__ == '__main__' :
        Main()
