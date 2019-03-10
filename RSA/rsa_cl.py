from Crypto.PublicKey import RSA
from Crypto import Random
import pickle
import socket
import time
import statistics
import math
import datetime as dt

HOST = socket.gethostbyname(socket.gethostname())
PORT = 2001
MESSAGE = "Hello"
count = 0
round_trip_time = []

random_generator = Random.new().read
privatekey = RSA.generate(1024, random_generator)
publickey = privatekey.publickey()

with open('clientkey.txt', 'wb') as clientkey:
	pickle.dump(publickey, clientkey)

# Connect to TCP/IP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('Connecting to server ....', client_socket.getpeername())
print('Connection established ...', client_socket.getsockname())
print('---------')

with open('serverkey.txt', 'rb') as readserverkey:
	global server_publickey
	server_publickey = pickle.load(readserverkey)

endTime = time.time() + 60 * 5

while time.time() <= endTime:

	print(' \n--------  ',count+1,' ------- ')
	print(dt.datetime.now(),': client message sent .... ')

	start_round_time = time.time()
	cipher_text = server_publickey.encrypt(MESSAGE.encode('utf-8'), 32)[0]
	client_socket.sendall(cipher_text)

	return_data = client_socket.recv(1024)
	plain_text = privatekey.decrypt(return_data)
	plain_text = plain_text.decode('utf-8')
	round_trip_time.append(time.time() - start_round_time)

	print(dt.datetime.now(),': client received msg ...'+'"'+str(plain_text)+'"')

	count += 1
	time.sleep(2)

client_socket.close()
print('\n',dt.datetime.now(),': Connection closed ...\n')

avg = sum(round_trip_time)/len(round_trip_time)
std_dev = statistics.stdev(round_trip_time)
sqr_root = math.sqrt(len(round_trip_time))
conf_interval = 1.96 * (std_dev/sqr_root)

print('\n Confidence interval : %s' % conf_interval)
print('\n Average round_trip_time : %s' % avg)
print('\n avg + conf_interval = %s & avg - conf_interval = %s' % (avg+conf_interval, avg-conf_interval))


