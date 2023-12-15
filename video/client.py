# Welcome to PyShine
# lets make the client code
# Welcome to PyShine
# www.pyshine.com
import socket,cv2, pickle,struct
from time import time
from datetime import datetime

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '34.xxx' # Here Require CACHE Server IP
port = 4004
client_socket.connect((host_ip,port)) # a tuple
data = b""
payload_size = struct.calcsize("Q")
while True:
	while len(data) < payload_size:
		packet = client_socket.recv(4*1024) # 4K
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
	current_timestamp = time()
	frame = cv2.putText(frame,str(datetime.fromtimestamp(current_timestamp)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,0), 1, cv2.LINE_AA)
				
	cv2.imshow("RECEIVING VIDEO FROM CACHE SERVER",frame)
	key = cv2.waitKey(1) & 0xFF
	if key  == ord('q'):
		break
client_socket.close()
	

