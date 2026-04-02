import pygame
import time
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
	def draw(self, drawable_object, coordinates):
		self.screen.blit(drawable_object, coordinates)
	def fill(self, color):
		self.screen.fill(color)
	def update(self):
		pygame.display.flip()
		self.clear()
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_F11:
					self.fullscreen = not self.fullscreen
					if self.fullscreen:
						self.screen = pygame.display.set_mode(self.screen_size, pygame.FULLSCREEN | pygame.HWSURFACE)
					else:
						self.screen = pygame.display.set_mode(self.screen_size, pygame.HWSURFACE)
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

class Image:
	def __init__(self, path):
		self.image = pygame.image.load(path).convert_alpha()
	def get_image(self):
		return self.image
	def get_rect(self):
		return self.image.get_rect()
	def get_width(self):
		return self.image.get_width()
	def get_height(self):
		return self.image.get_height()
	def get_size(self):
		return self.image.get_size()
	def transform_scale(self, width, height):
		self.image = pygame.transform.scale(self.image, (width, height))

class Mouse:
	def __init__(self):
		self.mouse_pos = pygame.mouse.get_pos()
		self.left_pressed = pygame.mouse.get_pressed()[0]
		self.middle_pressed = pygame.mouse.get_pressed()[1]
		self.right_pressed = pygame.mouse.get_pressed()[2]
	def get_pos(self):
		return self.mouse_pos
	def get_left_pressed(self):
		return self.left_pressed
	def get_middle_pressed(self):
		return self.middle_pressed
	def get_right_pressed(self):
		return self.right_pressed
	def update(self):
		self.mouse_pos = pygame.mouse.get_pos()
		self.left_pressed = pygame.mouse.get_pressed()[0]
		self.middle_pressed = pygame.mouse.get_pressed()[1]
		self.right_pressed = pygame.mouse.get_pressed()[2]

class Button:
	def __init__(self, image, x, y, command, command_hovered, command_back, mouse):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.x = x
		self.y = y
		self.command = command
		self.command_hovered = command_hovered
		self.command_back = command_back
		self.mouse = mouse
	def get_rect(self):
		return self.rect
	def get_image(self):
		return self.image.get_image()
	def switch_image(self, image):
		self.image = image
		self.rect = self.image.get_rect()
		self.rect.topleft = (self.x, self.y)
	def update(self):
		if self.rect.collidepoint(self.mouse.get_pos()):
			self.command_hovered()
			if self.mouse.get_left_pressed():
				self.command()
		else:
			self.command_back()

class SceneManager:
	def __init__(self):
		self.scene = None
		self.subscene = None
	def set_scene(self, scene):
		self.scene = scene
	def set_subscene(self, subscene):
		self.subscene = subscene
	def get_scene(self):
		return self.scene
	def get_subscene(self):
		return self.subscene

class FPSContoller:
	def __init__(self, max_fps=60):
		self.max_fps = max_fps
		self.fps_controller = pygame.time.Clock()
		self.fps_controller.tick(self.max_fps)
		self.frame_count = 0
		self.real_fps = 0
		self.last_time = time.time()
	def get_max_fps(self):
		return self.max_fps
	def get_real_fps(self):
		if time.time() - self.last_time >= 1.0:
			self.real_fps = self.frame_count
#			print(f"FPS: {self.real_fps}")
			self.frame_count = 0
			self.last_time = time.time()
	def set_max_fps(self, max_fps):
		self.max_fps = max_fps
		self.fps_controller.tick(self.max_fps)
	def update(self):
		self.frame_count += 1
		self.fps_controller.tick(self.max_fps)

def play_hovered():
	global play_button
	play_button.switch_image(Image("resources/images/play_button_hovered.png"))

def play_command():
	global click_sound
	click_sound.play()

def play_back():
	global play_button
	play_button.switch_image(Image("resources/images/play_button.png"))

WIDTH, HEIGHT = 640, 480
window = Window("AngryBirds", WIDTH, HEIGHT)

scenes = SceneManager()
scenes.set_scene("menu")

fps = FPSContoller()

mouse = Mouse()

theme_sound = Sound("resources/sounds/background.mp3", "infinity")
theme_sound.set_volume(0.1)

click_sound = Sound("resources/sounds/click.mp3")

background_image = Image("resources/images/menu_background.png")

play_image = Image("resources/images/play_button.png")
play_button = Button(play_image, WIDTH // 2 - play_image.get_width() // 2, HEIGHT // 2 - play_image.get_height() // 2, play_command, play_hovered, play_back, mouse)

if __name__ == "__main__":
    while True:
        if not theme_sound.get_busy():
            theme_sound.play()
        if scenes.get_scene() == "menu":
            window.draw(background_image.get_image(), (0, 0))
            window.draw(play_button.get_image(), play_button.get_rect())
            play_button.update()
        fps.update()
        fps.get_real_fps()
        mouse.update()
        window.update()