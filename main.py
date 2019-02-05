import pygame
import os
import sys


pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ChooseBrick")
version = "0.0.1"

def load_image(name, colorkey=None):
	fullname = os.path.join("data", name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		print("Cannot load the image")
		raise SystemExit(message)
	image = image.convert_alpha()
	if colorkey is not None:
		if colorkey == -1:
			colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey)
	return image


background_image = load_image('background_image.jpg')


runing = True
all_sprites = pygame.sprite.Group()

while runing:
	screen.blit(background_image, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			runing = False

	all_sprites.draw(screen)
	pygame.display.flip()

pygame.quit()
sys.exit()