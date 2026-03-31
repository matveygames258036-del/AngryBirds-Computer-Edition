import pygame
import sys

pygame.init()

class Window:
	def __init__(self, title, screen_width, screen_height):
		self.fullscreen = False
		self.screen_size = (screen_width, screen_height)
		self.screen = pygame.display.set_mode(self.screen_size)
		self.CLEAR_COLOR = (0, 0, 0)
		pygame.display.set_caption(title)
	def clear(self):
		self.screen.fill(self.CLEAR_COLOR)
	def draw(self, drawable_object, x, y):
		self.screen.blit(drawable_object, (x, y))
	def fill(self, color):
		self.screen.fill(color)
	def update(self):
		self.clear()
		pygame.display.flip()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F11:
					self.fullscreen = not self.fullscreen
					if self.fullscreen:
						self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN)
					else:
						self.screen = pygame.display.set_mode(self.screen_size)
			if event.type == pygame.QUIT:
				sys.exit()

class Sound:
	def __init__(self, path, sound_type="normal"):
		self.sound_type = sound_type
		if self.sound_type == "normal":
			self.sound = pygame.mixer.Sound(path)
		elif self.sound_type == "infinity":
			self.sound = pygame.mixer.Sound(path)
			self.channel = pygame.mixer.Channel(0)
		else:
			raise(TypeError("Unknown sound type"))
	def play(self):
		if self.sound_type == "normal":
			self.sound.play()
		elif self.sound_type == "infinity":
			self.channel.play(self.sound)
	def stop(self):
	    if self.sound_type == "infinity":
	        self.channel.stop()
	    else:
	        self.sound.stop()
	def get_busy(self):
		if self.sound_type == "infinity":
			return self.channel.get_busy()
		else:
			raise(TypeError("This is not infinity sound type"))
	def set_volume(self, volume):
		if self.sound_type == "infinity":
			self.channel.set_volume(volume)
		else:
			self.sound.set_volume(volume)

window = Window("AngryBirds", 640, 480)

theme_sound = Sound("resources/sounds/background.mp3", "infinity")
theme_sound.set_volume(0.5)

while True:
	if not theme_sound.get_busy():
		theme_sound.play()
	window.update()