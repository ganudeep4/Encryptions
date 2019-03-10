import socket
import datetime as dt
from Crypto.Cipher import DES

HOST = socket.gethostbyname(socket.gethostname())
PORT = 2001
MESSAGE = "Nice to see you"
count = 0


# Connect to TCP/IP Socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.settimeout(10)
server_socket.listen(1)

des = DES.new('ganudeep', DES.MODE_ECB)
PADDING = '{'

padded_text = MESSAGE + ((8-len(MESSAGE) % 8) * PADDING)


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
			plain_text = des.decrypt(cipher_text)
			plain_text = plain_text.strip(b"{")

			if plain_text.lower() == b'hello':
				i = 0
				print(' \n--------  ',count+1,' ------- ')
				print(dt.datetime.now(),': server received ... '+plain_text.decode('ascii'))
				count += 1
				while i < len(padded_text):
					return_cipher = des.encrypt(padded_text[i:i+8])
					print(dt.datetime.now(),': server msg sending 8 bytes at time ... ')
					conn.sendall(return_cipher)
					i += 8

			if not cipher_text:
				break


	finally:
		# Closing the connection
		print('\n',dt.datetime.now(),': Closing connection ....\n','----------------------------------------------------')
		conn.close()
