# This code will run the drone side, it will send video to cache server
# Lets import the libraries
# Welcome to PyShine
# www.pyshine.com
import socket, cv2, pickle, struct
import imutils
from time import time
from datetime import datetime
import sys

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = '192.xxx' # Enter the Drone IP address
print('HOST IP:',host_ip)
port = 4000
socket_address = (host_ip,port)
server_socket.bind(socket_address)
server_socket.listen()
print("Listening at",socket_address)

def start_video_stream():
	client_socket,addr = server_socket.accept()
	camera = True
	if camera == True:
		vid = cv2.VideoCapture(0)
	try:
		print('CLIENT {} CONNECTED!'.format(addr))
		if client_socket:
			while(vid.isOpened()):
				img,frame = vid.read()

				frame  = imutils.resize(frame,width=320)
				# print(frame.shape)
				current_timestamp = time()
				frame = cv2.putText(frame,str(datetime.fromtimestamp(current_timestamp)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1, cv2.LINE_AA)
				
				a = pickle.dumps(frame)
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
				# print(message)
				cv2.imshow("TRANSMITTING TO CACHE SERVER",frame)
				key = cv2.waitKey(1) & 0xFF
				if key ==ord('q'):
					client_socket.close()
					break

	except Exception as e:
		print(f"CACHE SERVER {addr} DISCONNECTED")
		pass

while True:
	start_video_stream()


