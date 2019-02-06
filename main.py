import pygame
import os
import sys


pygame.init()
size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ChooseBrick")
version = "0.0.1"

class StopMovingError(Exception):
	pass

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

class Board():

	def __init__(self, x, y, top, left, cell_size):
		self.x = x
		self.y = y
		self.top = top
		self.left = left
		self.cell_size = cell_size
		self.board = [[0] * self.x for i in range(self.y)]
		self.maxnum = 0
		self.blocklist = []

	def render(self):
		for i in range(self.x):
			for j in range(self.y):
				pygame.draw.rect(screen,
					pygame.Color('black'),
					(self.left + self.cell_size * i, self.top + self.cell_size * j, self.cell_size, self.cell_size), 1)

	def loadlevel(self, level_lines):
		self.board = level_lines

	def get_cell(self, coords):
		x = coords[0]
		y = coords[1]
		x_cell = (x - self.left) // self.cell_size
		y_cell = (y - self.top) // self.cell_size
		return x_cell, y_cell


	def get_brick(self, cell_coords, coords):
		for block in self.blocklist:
			if block.number == self.board[cell_coords[0]][cell_coords[1]]:
				needed_block = block
		try:
			a = needed_block
		except Exception:
			print('Cannot find a block')
		else:
			return needed_block

class MenuBlock(pygame.sprite.Sprite):

	def __init__(self, board):
		self.x = 2
		self.y = 3
		self.length = 2
		self.board = board
		self.orientation = 0
		self.number = self.board.maxnum + 1
		self.board.maxnum += 1
		if self.orientation == 0:
			for i in range(self.length):
				# print(self.x + self.length)
				self.board.board[self.x + i][self.y] = self.number
			# print(self.board.board)
		elif self.orientation == 1:
			for i in range(self.length):
				self.board.board[self.x][self.y + i] = self.number
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image('menu_brick_texture.jpg')
		self.rect = self.image.get_rect()
		self.rect.x = self.x * self.board.cell_size + self.board.left
		self.rect.y = self.y * self.board.cell_size + self.board.top
		self.add_to_group(block_sprites)


	def add_to_group(self, group):
		group.add(self)
		self.board.blocklist.append(self)
		print('done')

	def move(self, delta):
		# print(str(self), 'need to move')
		self.rect.x += delta[0]
	

	def update(self, delta):
		try:
			self.move(delta)
			if pygame.sprite.spritecollideany(self, horizontal_borders):
				raise StopMovingError
			if pygame.sprite.spritecollideany(self, vertical_borders):
				raise StopMovingError
		except StopMovingError:
			# print('вот гавно')
			delta = -1 * delta[0], -1 * delta[1]
			self.update(delta)

	def finish_moving(self):
		self.rect.x = 

	def __str__(self):
		return str(self.number) + 'MENU BLOCK'

def loadLevel(level_number):
	global board
	filename = str(level_number) + 'level.txt'
	with open(file, encoding='utf-8') as file:	
		lines = [i.split() for i in file.readlines()]
	board.loadlevel(lines)

def create_borders():
	vertical_border = pygame.sprite.Sprite()
	vertical_border.image = load_image("vertical.jpg")
	vertical_border.rect = vertical_border.image.get_rect()
	vertical_border.rect.x = 50
	vertical_border.rect.y = 50
	vertical_borders.add(vertical_border)
	vertical_border2 = pygame.sprite.Sprite()
	vertical_border2.image = load_image("vertical.jpg")
	vertical_border2.rect = vertical_border2.image.get_rect()
	vertical_border2.rect.x = 540
	vertical_border2.rect.y = 50
	vertical_borders.add(vertical_border2)
	horizontal_border = pygame.sprite.Sprite()
	horizontal_border.image = load_image("horizontal.jpg")
	horizontal_border.rect = horizontal_border.image.get_rect()
	horizontal_border.rect.x = 60
	horizontal_border.rect.y = 50
	horizontal_borders.add(horizontal_border)
	horizontal_border2 = pygame.sprite.Sprite()
	horizontal_border2.image = load_image("horizontal.jpg")
	horizontal_border2.rect = horizontal_border2.image.get_rect()
	horizontal_border2.rect.x = 60
	horizontal_border2.rect.y = 540
	horizontal_borders.add(horizontal_border2)


background_image = load_image('background_image.jpg')

runing = True
block_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
create_borders()
board = Board(6, 6, 60, 60, 80)
menublock = MenuBlock(board)
moving = 0
brick = None

while runing:
	screen.blit(background_image, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			runing = False
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos[0] in range(60, 541) and event.pos[1] in range(60, 541):
				cell = board.get_cell(event.pos)
				brick = board.get_brick(cell, event.pos)
				if brick != None:
					moving = brick.number
				else:
					moving = 0
				LP = event.pos

		elif event.type == pygame.MOUSEBUTTONUP:
			moving = 0
			if brick is not None:
				brick.finish_moving()
				brick = None

		elif event.type == pygame.MOUSEMOTION:
			if brick is not None:
				delta = event.pos[0] - LP[0], event.pos[1], LP[1]
				LP = event.pos
				brick.update(delta)

		elif event.type == pygame.KEYDOWN:
			if event.unicode == 'b':
				print(board.board)

	board.render()
	block_sprites.draw(screen)
	vertical_borders.draw(screen)
	horizontal_borders.draw(screen)
	pygame.display.flip()

pygame.quit()
sys.exit()