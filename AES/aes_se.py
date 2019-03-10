import socket
import datetime as dt
from Crypto.Cipher import AES


HOST = socket.gethostbyname(socket.gethostname())
PORT = 2001
MESSAGE = "Nice to see you"
count = 0


# Connect to TCP/IP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.settimeout(10)
server_socket.listen(1)


KEY = 'Name is ganudeep'
IV = 'Find python job.'
aes_set = AES.new(KEY, AES.MODE_CBC, IV)

PADDING = '{'
padded_text = MESSAGE + ((16-len(MESSAGE) % 16) * PADDING)


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
		while True:
			cipher_text = conn.recv(50)
			plain_text = aes_set.decrypt(cipher_text)
			plain_text = plain_text.strip(b'{')

			if plain_text.lower() == b'hello':
				print(' \n--------  ',count+1,' ------- ')
				print(dt.datetime.now(),': server received msg... '+plain_text.decode('ascii'))
				count += 1
				return_cipher = aes_set.encrypt(padded_text)
				print(dt.datetime.now(),': server sending msg... ')
				conn.sendall(return_cipher)

			if not cipher_text:
				break

	finally:
		
		# Closing the connection
		print('\n',dt.datetime.now(),': Closing connection ....\n','----------------------------------------------------')
		conn.close()
