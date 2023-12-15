# TODO
# -external message iput
# -external message log
# -extra button for additional something


import socket,cv2, pickle,struct
import pygame
import numpy as np
import threading
import time


BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)


print("[**] Client UNIT")

# PYGAME 
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock()
joystick = pygame.joystick.Joystick(0)
joystick.init()
print("[*]Joystick connected")
name = joystick.get_name()
print(f"[*]Joystick name: {name}")
power_level = joystick.get_power_level()
print(f"[*]Joystick's power level: {power_level}")

font = pygame.font.SysFont("Consolas", 20)
font_log = pygame.font.SysFont("Consolas", 18)
screen_size = [640, 250]
screen = pygame.display.set_mode(screen_size)
ada = True 
running = True

# STEERING 
a = pygame.sprite.Sprite()
a.image = pygame.Surface((20, 100))
a.image.set_colorkey(BLACK)
a.image.fill(WHITE)
a.rect = a.image.get_rect()
a.rect.topleft = (320+50, 120-50)
a.orig_image = a.image
a_group = pygame.sprite.Group()
a_group.add(a)
position1 = (a.rect.centerx, a.rect.centery)
angle = 0

# text input
font = pygame.font.Font(None, 32)
clock = pygame.time.Clock()
log_box = pygame.Rect(450, 5, 190, 240-32-10-10)
input_box = pygame.Rect(log_box.x, log_box.y + log_box.h+10, log_box.w, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
text_log = 'Command Log'
done = False


#default Park
extra_command = ''
message = [1000,1,1,extra_command]
[steering, pedal, gear, extra_command] = message

def print_log(content):
	global text_log
	text_log += '\n'+content
	print(content)

def get_control_data(extra_command):			#need to import in main loop
	global message
	[steering, pedal, gear, extra_command] = message

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

def remap_steering(raw_steering):				#Mapping 0-2000 to given angle(RightEnd to LeftEnd)  
	max_angle = 270    ##############MODIFY NEEDED
	weight = max_angle/2000
	return -(raw_steering * weight)+(max_angle/2)

def convert_opencv_img_to_pygame(opencv_image):
	opencv_image = opencv_image[:,:,::-1]  
	shape = opencv_image.shape[1::-1]  
	pygame_image = pygame.image.frombuffer(opencv_image.tobytes(), shape, 'RGB')
	return pygame_image

def get_vid():		#getting vid from video_cache server
	global frame
	host_ip_v = '34.xxxxx' # Video-Server IP
	port_v = 4004
	data = b""
	payload_size = struct.calcsize("Q")
	while True:
		try:
			client_socket_v = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			client_socket_v.connect((host_ip_v,port_v)) 

			while True:
				while len(data) < payload_size:
					packet = client_socket_v.recv(3*1024)
					if not packet: break
					data+=packet
				
				packed_msg_size = data[:payload_size]
				data = data[payload_size:]
				msg_size = struct.unpack("Q",packed_msg_size)[0]
				
				while len(data) < msg_size:
					data += client_socket_v.recv(3*1024)
				
				frame_data = data[:msg_size]
				data  = data[msg_size:]
				frame = pickle.loads(frame_data)
					
				
				
		except Exception as e:
			print_log(f"[*]VS DISCONNECTED")#video server disconnected
			pass

def send_data():
	global extra_command
	global message
	server_socket_c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	host_name_c  = socket.gethostname()
	host_ip_c = '192.xxxxx' # Client IP address
	print('HOST IP:',host_ip_c)
	port_c = 5000
	socket_address_c = (host_ip_c,port_c)
	server_socket_c.bind(socket_address_c)
	server_socket_c.listen()
	print("Listening at",socket_address_c)



	while True:
		client_socket,addr = server_socket_c.accept()

		try:
			# print_log('CONTROL-SERVER {} CONNECTED!'.format(addr))
			print_log('[*]CS CONNECTED!')
			
			while True:
				m = str(message)
				client_socket.sendall(m.encode())
				# print(message)
				extra_command = ''
				time.sleep(0.2)

		except Exception as e:
			print_log(f"[*]CS DISCONNECTED")
			pass

def text_newline(surface, text, pos, font, color=pygame.Color('white')):
	if len(text.splitlines()) > 7:
		text = '\n'.join(text.splitlines()[-7:])
		
	words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
	space = font.size(' ')[0]  # The width of a space.
	max_width, max_height = surface.get_size()
	x, y = pos
	for line in words:
		for word in line:
			word_surface = font.render(word, 0, color)
			word_width, word_height = word_surface.get_size()
			if x + word_width >= max_width:
				x = pos[0]  # Reset the x.
				y += word_height  # Start on new row.
			surface.blit(word_surface, (x, y))
			x += word_width + space
		x = pos[0]  # Reset the x.
		y += word_height  # Start on new row.



thread_v = threading.Thread(target=get_vid, args=())
thread_c = threading.Thread(target=send_data, args=())
thread_v.start()
thread_c.start()

##########

while running==True :
	screen.fill(BLACK)
	
	for event in pygame.event.get(): 
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONDOWN:
			# If the user clicked on the input_box rect.
			if input_box.collidepoint(event.pos):
				# Toggle the active variable.
				active = not active
			else:
				active = False
			# Change the current color of the input box.
			color = color_active if active else color_inactive
		if event.type == pygame.KEYDOWN:
			if active:
				if event.key == pygame.K_RETURN:
					extra_command = text
					text_log += '\n> '+ text
					text = ''
				elif event.key == pygame.K_BACKSPACE:
					text = text[:-1]
				else:
					text += event.unicode


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


# text input
	txt_surface = font.render(text, True, color)
	txt_log_surface = font.render(text_log, True, color)
	screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
	text_newline(screen, text_log, (log_box.x+5, log_box.y+5), font_log)
	
	# Blit the input_box rect.
	pygame.draw.rect(screen, color, input_box, 2)
	pygame.draw.rect(screen, color, log_box, 2)







	message = [int(steering), pedal, gear,extra_command]		
	
	steering = message[0]
	pedal = message[1]
	gear = message[2]

	if pedal == 0:
		pedal_t = 'brake'
	elif pedal == 1:
		pedal_t = '-'
	else:
		pedal_t = 'gas'

	if gear == 0:
		gear_t = 'R'
	elif gear == 1:
		gear_t = 'P'
	elif gear == 2:
		gear_t = 'D'

	# DRAW GEAR & PEDAL STATUES
	pedal_statue = font.render(pedal_t, True, WHITE)
	gear_statue = font.render(gear_t, True, WHITE)
	screen.blit(pedal_statue, [5, 25,])
	screen.blit(gear_statue, [5, 45,])
	
	# DRAW STEERING WHEEL
	ui_steering = round(remap_steering(steering)) 
	pygame.draw.circle(screen, WHITE, position1, 50, 2)
	pygame.draw.rect(screen, WHITE, (320+50, 120-50,20,100), 1)   #Origin rect
	a_group.draw(screen)
	orig_center = a.rect.center  # Save original center of sprite.
	# Rotate using the original image.
	a.image = pygame.transform.rotate(a.orig_image, ui_steering)
	# Get the new rect and set its center to the original center.
	a.rect = a.image.get_rect(center=orig_center)

	try:
		# cv2.imshow("RECEIVING VIDEO FROM CACHE SERVER",frame)
	
		pygame_frame = convert_opencv_img_to_pygame(frame)
		if ada == True :
			h=pygame_frame.get_height()
			w=pygame_frame.get_width()
			screen = pygame.display.set_mode([640, h])
			ada = False

		screen.blit(pygame_frame, (0, 0))  
		screen.blit(pedal_statue, [w+5, 5,])
		screen.blit(gear_statue, [w+85, 5,])
	except:
		video_statue = font.render("NO VIDEO SIGNAL :/", True, WHITE)
		screen.blit(video_statue, [5, 5,])
		
	
	clock.tick(30)
	pygame.display.update()
	
	

