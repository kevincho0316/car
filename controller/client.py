# client

'''
[steering, pedal, gear]
-steering 000-2000
-pedal 0=brake 1=n/a 2=gas
-gear  0=R 1=P 2=D
'''

import socket
import time
import pygame



server_socket_c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name_c  = socket.gethostname()
host_ip_c = '192.xxx' # Enter the client IP address
print('HOST IP:',host_ip_c)
port_c = 5000
socket_address_c = (host_ip_c,port_c)
server_socket_c.bind(socket_address_c)
server_socket_c.listen()
print("Listening at",socket_address_c)

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("[*]Joystick connected")
name = joystick.get_name()
print(f"[*]Joystick name: {name}")
power_level = joystick.get_power_level()
print(f"[*]Joystick's power level: {power_level}")
gear = 1       #default Park
pedal = 1
steering = 1000
extra_command = 'extra_command'

def get_control_data(extra_command):
	global pedal
	global steering
	global gear

	for event in pygame.event.get():
		
		if event.type == pygame.JOYAXISMOTION:
			steering = joystick.get_axis(0) + 1
			steering = (round(steering,3) * 1000)
		if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYBUTTONUP:
			brake =  joystick.get_button(6)
			gas = joystick.get_button(7)
			D = joystick.get_button(0)
			P = joystick.get_button(1)
			R = joystick.get_button(2)
			if D==1:
				gear = 2
			elif R==1:
				gear = 0
			elif P==1:
				gear = 1
	
			if brake == 1 and gas == 1:
				pedal = 0      
			else:
				pedal = 1-brake+gas

	return [int(steering), pedal, gear,extra_command]



def send_data(extra_command):
	client_socket,addr = server_socket_c.accept()

	try:
		print('CACHE SERVER {} CONNECTED!'.format(addr))
		while True:
			message = str(get_control_data(extra_command))
			client_socket.sendall(message.encode())
			print(message)
			time.sleep(0.2)

	except Exception as e:
		print(f"CACHE SERVER {addr} DISCONNECTED")
		pass

while True:
	send_data(extra_command)
	

