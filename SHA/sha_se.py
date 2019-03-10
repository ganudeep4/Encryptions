import socket
import datetime as dt
import sha3

HOST = socket.gethostbyname(socket.gethostname())
PORT = 2001
SER_MSG = b"Nice to see you"
CLI_MSG = 'Hello'
count = 0


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.settimeout(10)
server_socket.listen(1)


while True:
	print()

	try:
		print(dt.datetime.now(),': waiting for connection ...', server_socket.getsockname())
		conn, address = server_socket.accept()
		print(dt.datetime.now(),': connection established from.....', conn.getpeername())

	except:
		print('connection timeout.')
		break

	try:
		sha_cli_msg = sha3.sha3_224(CLI_MSG.encode('utf-8')).hexdigest()
		while True:
			cipher_text = conn.recv(1024).decode('utf-8')

			if (cipher_text == sha_cli_msg):
				print(' \n--------  ',count+1,' ------- ')
				print(dt.datetime.now(),': server received msg... Hello')

				count += 1

				print(dt.datetime.now(),': server sending msg .... ')
				return_cipher = sha3.sha3_224(SER_MSG).hexdigest()
				conn.sendall(return_cipher.encode('utf-8'))


			if not cipher_text:
				break



	finally:
		# Closing the connection
		print('\n',dt.datetime.now(),': Closing connection ....\n','----------------------------------------------------')
		conn.close()
