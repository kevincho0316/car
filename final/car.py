# sudo kill -4000 5004
import socket, cv2, pickle, struct
import threading
import imutils
import cv2
import ast

print('[**]Car UNIT')
server_socket_v = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name_v  = socket.gethostname()
host_ip_v = '192.xxx' # internal car ip
print('[*]HOST IP:',host_ip_v)
port_v = 4000
socket_address_v = (host_ip_v,port_v)
server_socket_v.bind(socket_address_v)
server_socket_v.listen()
print("[*]Listening at",socket_address_v)

font =  cv2.FONT_HERSHEY_PLAIN
 


def receiving_data():
	global global_message
	client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_ip = '34.xxx' # Control-Server IP
	port = 5004
	client_socket.connect((host_ip,port)) 
	data = b""
	while True:
		try:
			while True:
				data = client_socket.recv(1024)
				data = data.decode()
				try:
					data = data.split('][')		
					
					message = '['+data[1]+']'
				except:
					message=data[0]
				if ']]' in message:		
						message = message.replace(']]', ']')
				ast.literal_eval(message)
				global_message = message
				print(message)				#DEBUGGING ONLY
				
				# message = [steering, pedal, gear, extra]
				steering = message[0]		#-steering 000-2000
				pedal = message[1]			#-pedal 0=brake 1=n/a 2=gas
				gear = message[2]			#-gear  0=R 1=P 2=D
				extra_command = message[3]
				
				
		except Exception as e:
			print(f"[*]control CACHE SERVER DISCONNECTED")
			pass

def start_video_stream():
	global global_message
	client_socket,addr = server_socket_v.accept()
	camera = True
	if camera == True:
		vid = cv2.VideoCapture(0)
	try:
		print('[*]Video-server {} CONNECTED!'.format(addr))
		if client_socket:
			while(vid.isOpened()):
				img,frame = vid.read()

				frame  = imutils.resize(frame,width=320)
				a = pickle.dumps(frame)
				message = struct.pack("Q",len(a))+a
				client_socket.sendall(message)
				
			
				if global_message != None:
					frame = cv2.putText(frame, global_message, (50, 50), font, 2, (0,0,0), 1, cv2.LINE_AA)
				cv2.imshow("[*]TRANSMITTING TO CACHE SERVER",frame) #DEBUGGING ONLY
				
				key = cv2.waitKey(1) & 0xFF
				if key ==ord('q'):
					client_socket.close()
					break

	except Exception as e:
		print(f"[*]video CACHE SERVER {addr} DISCONNECTED")
		pass


video = threading.Thread(target=start_video_stream, args=())
video.start()
control = threading.Thread(target=receiving_data, args=())
control.start()
	
	


