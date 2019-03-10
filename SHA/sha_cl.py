import socket
import time
import datetime as dt
import sha3
import statistics
import math

HOST = socket.gethostbyname(socket.gethostname())
PORT = 2001
CLI_MSG = b"Hello"
SER_MSG = 'Nice to see you'
count = 0
round_trip_time = []

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
	sha_cli_msg = sha3.sha3_224(CLI_MSG).hexdigest()
	client_socket.sendall(sha_cli_msg.encode('utf-8'))

	return_data = client_socket.recv(1024).decode('utf-8')
	sha_ser_msg = sha3.sha3_224(SER_MSG.encode('utf-8')).hexdigest()

	if (sha_ser_msg == return_data):
		round_trip_time.append(time.time() - start_round_time)
		print(dt.datetime.now(),': client received msg ... Nice to see you')

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

