import pygame 

def text_newline(surface, text, pos, font, color=pygame.Color('black')):
	if len(text.splitlines()) > 7:
		text = '\n'.join(text.splitlines()[-6:])
		
		
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

def main():
	screen = pygame.display.set_mode((640, 480))
	font = pygame.font.Font(None, 32)
	clock = pygame.time.Clock()
	log_box = pygame.Rect(0, 0, 190, 300)
	input_box = pygame.Rect(log_box.x, log_box.y + log_box.h+10, log_box.w, 32)
	color_inactive = pygame.Color('lightskyblue3')
	color_active = pygame.Color('dodgerblue2')
	color = color_inactive
	active = False
	text = ''
	text_log = ''
	done = False

	while not done:
		screen.fill((30, 30, 30))
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
						text_log += '\n> '+ text
						text = ''
					elif event.key == pygame.K_BACKSPACE:
						text = text[:-1]
					else:
						text += event.unicode

		# Render the current text.
		txt_surface = font.render(text, True, color)
		txt_log_surface = font.render(text_log, True, color)
		# Resize the box if the text is too long.
		# input_box.w = max(200, txt_surface.get_width()+10)
		# Blit the text.
		screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
		# screen.blit(txt_log_surface, (log_box.x+5, log_box.y+5))
		text_newline(screen, text_log, (log_box.x+5, log_box.y+5), font)
		
		# Blit the input_box rect.
		pygame.draw.rect(screen, color, input_box, 2)
		pygame.draw.rect(screen, color, log_box, 2)

		pygame.display.flip()
		clock.tick(30)


if __name__ == '__main__':
	pygame.init()
	main()
	pygame.quit()