import socket
import datetime as dt
import time
import statistics
import math
from Crypto.Cipher import DES

HOST = socket.gethostbyname(socket.gethostname())
PORT = 2001
MESSAGE = "Hello"
count = 0
round_trip_time = []

des = DES.new('ganudeep', DES.MODE_ECB)
PADDING = '{'

padded_text = MESSAGE + ((8-len(MESSAGE) % 8) * PADDING)

# Connect to TCP/IP Socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print('Connecting to server ....', client_socket.getpeername())
print('Connection established ...', client_socket.getsockname())
print('---------')

endTime = time.time() + 60 * 5

while time.time() <= endTime:

	print(' \n--------  ',count+1,' ------- ')
	print(dt.datetime.now(),': client message sent .... ')

	start_round_time = time.time()
	cipher_text = des.encrypt(padded_text)
	client_socket.sendall(cipher_text)

	return_data = client_socket.recv(50)
	return_data = des.decrypt(return_data)
	return_data = return_data.strip(b"{")
	round_trip_time.append(time.time() - start_round_time)
	print(dt.datetime.now(),': client received ...'+'"'+return_data.decode('ascii')+'"')

	count += 1
	time.sleep(2)


client_socket.close()
# print('\n',dt.datetime.now(),': Connection closed ...\n')


avg = sum(round_trip_time)/len(round_trip_time)
std_dev = statistics.stdev(round_trip_time)
sqr_root = math.sqrt(len(round_trip_time))
conf_interval = 1.96 * (std_dev/sqr_root)

print('\n Confidence interval : %s' % conf_interval)
print('\n Average round_trip_time : %s' % avg)
print('\n avg plus = %s & avg minus = %s' % (avg+conf_interval, avg-conf_interval))