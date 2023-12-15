
import socket, pickle, struct
# import imutils # pip install imutils
import threading
import time

# import cv2


server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 5004
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

global message
message = None

def start_video_stream():
	global message
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_ip = '125.xxx' # Here provide Drone IP 
	port = 5000
	data = b""
	client_socket.connect((host_ip,port))
	while True:
		data = client_socket.recv(1024)
		data = data.decode().split('][')		#oh god
		
		try:
			message = '['+data[1]+']'
		except:
			message=data[0]
		
		
		if ']]' in message:		
			s = s.replace(']]', ']')
			print(data)
			print(message)
			print("#############")

		print(message)
		
		# if key  == ord('q'):
		# 	break
	client_socket.close()
	

thread = threading.Thread(target=start_video_stream, args=())
thread.start()

def serve_client(addr,client_socket):
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket:
			while True:
				client_socket.sendall(message.encode())
				time.sleep(0.2)
				
	except Exception as e:
		print(f"CLINET {addr} DISCONNECTED")
		pass

   
while True:
	client_socket,addr = server_socket.accept()
	print(addr)
	thread = threading.Thread(target=serve_client, args=(addr,client_socket))
	thread.start()
	print("TOTAL CLIENTS ",threading.activeCount() - 2) # edited here because one thread is already started before


