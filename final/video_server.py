# kill -9 4000
import socket, pickle, struct
import threading
import cv2
import time

print("[**] VIDEO-SERVER UNIT")

video_save = True

saved = True



server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 4004
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

global frame
frame = None

def save_data():
	global saved
	global frame
	while True:
		if saved == False :
			timestr = time.strftime("%Y%m%d-%H%M%S")
			cv2.imwrite("./log/video/%s.jpg" % timestr, frame )
			saved = True

def start_video_stream():
	global frame
	global saved
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_ip = '125.xxxxx' # CAR EXTERNAL IP 
	port = 4000
	client_socket.connect((host_ip,port))
	data = b""
	payload_size = struct.calcsize("Q")
	while True:
		while len(data) < payload_size:
			packet = client_socket.recv(3*1024) 
			if not packet: break
			data+=packet
		packed_msg_size = data[:payload_size]
		data = data[payload_size:]
		msg_size = struct.unpack("Q",packed_msg_size)[0]
		
		while len(data) < msg_size:
			data += client_socket.recv(3*1024)
		frame_data = data[:msg_size]
		data  = data[msg_size:]
		frame = pickle.loads(frame_data)
		saved = False
		# cv2.imshow("RECEIVING VIDEO FROM DRONE",frame)
		# key = cv2.waitKey(1) & 0xFF
		# print(data)
		# if key  == ord('q'):
		# 	break
	client_socket.close()

def serve_client(addr,client_socket):
	global frame
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket:
			while True:
				a = pickle.dumps(frame)
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
				
	except Exception as e:
		print(f"CLINET {addr} DISCONNECTED")
		pass

t_start_video_stream = threading.Thread(target=start_video_stream, args=())
t_start_video_stream.start()

if video_save == True:
	print("[*] VIDEO SAVING")
	t_save_data = threading.Thread(target=save_data, args=())
	t_save_data.start()

   
while True:
	client_socket,addr = server_socket.accept()
	print(addr)
	thread = threading.Thread(target=serve_client, args=(addr,client_socket))
	thread.start()
	print("TOTAL CLIENTS ",threading.activeCount() - 2) # edited here because one thread is already started before


