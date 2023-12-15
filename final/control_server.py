# sudo kill -9 $(sudo lsof -t -i:5004)
import socket
import threading
import time
import logging
# import cv2

print("[**] CONTROL-SERVER UNIT")

control_save = True

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO,
    datefmt='%m/%d/%Y %I:%M:%S %p',
	filename="./log/control/logfilename.log"
)


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('[*]HOST IP:',host_ip)
port = 5004
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("[*]Listening at",socket_address)

global message
message = None

def start_control_stream():
	global message
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_ip = '125.xxxx' # CAR EXTERNAL IP 
	port = 5000
	data = b""
	client_socket.connect((host_ip,port))
	while True:
		data = client_socket.recv(1024)
		data = data.decode().split('][')		#oh god
		
		try:
			data = '['+data[1]+']'
		except:
			message=data[0]

		if control_save == True: logging.info(message)
		# print(message)

	client_socket.close()
	

thread = threading.Thread(target=start_control_stream, args=())
thread.start()

def serve_client(addr,client_socket):
	try:
		print('[*]CAR {} CONNECTED!'.format(addr))
		if client_socket:
			while True:
				client_socket.sendall(message.encode())
				time.sleep(0.2)
				
	except Exception as e:
		print(f"[*]CAR {addr} DISCONNECTED")
		pass

   
while True:
	client_socket,addr = server_socket.accept()
	print(addr)
	thread = threading.Thread(target=serve_client, args=(addr,client_socket))
	thread.start()
	print("[*]TOTAL CAR ",threading.activeCount() - 2) # edited here because one thread is already started before
	