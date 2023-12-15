
import socket,cv2, pickle,struct
import ast

# create socket
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '35.xxx' # Here Require CACHE Server IP
port = 5004
client_socket.connect((host_ip,port)) # a tuple
data = b""
while True:
    data = client_socket.recv(1024)
    data = data.decode()
    try:
        data = data.split('][')		#oh god
        
        message = '['+data[1]+']'
    except:
        message=data[0]
    if ']]' in message:		
            message = message.replace(']]', ']')
    ast.literal_eval(message)
    print(message)
    
# client_socket.close()
	

