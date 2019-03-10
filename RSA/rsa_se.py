from Crypto.PublicKey import RSA
from Crypto import Random
import pickle
import socket
import datetime as dt

KEY_READ = False

HOST = socket.gethostbyname(socket.gethostname())
PORT = 2001
MESSAGE = "Nice to see you"
count = 0


random_generator = Random.new().read
privatekey = RSA.generate(1024, random_generator)
publickey = privatekey.publickey()

with open('serverkey.txt', 'wb') as serverkey:
	pickle.dump(publickey, serverkey)

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

		if not KEY_READ:
			with open('clientkey.txt', 'rb') as readclientkey:
				global client_publickey
				client_publickey = pickle.load(readclientkey)
			KEY_READ = True

		
		while True:
			cipher_text = conn.recv(1024)
			plain_text = privatekey.decrypt(cipher_text)
			plain_text = plain_text.decode('utf-8')			

			if plain_text.lower() == 'hello':
				print(' \n--------  ',count+1,' ------- ')
				print(dt.datetime.now(),': server received msg ...'+'"'+plain_text+'"')
				
				count += 1

				return_cipher = client_publickey.encrypt(MESSAGE.encode('utf-8'), 32)[0]
				conn.sendall(return_cipher)
				print(dt.datetime.now(),': server sending msg ...')

			if not cipher_text:
				break

	finally:
		# Closing the connection
		print('\n',dt.datetime.now(),': Closing connection ....\n','----------------------------------------------------')
		conn.close()



