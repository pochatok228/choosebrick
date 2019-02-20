import pygame
import os
import sys
import random
import json


pygame.init()
size = width, height = 600, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption("ChooseBrick")
version = "0.1.0"
click = pygame.mixer.Sound(os.path.join("data", "click.ogg"))
level_winner = pygame.mixer.Sound(os.path.join("data", "winner_level.ogg"))


def test_wait():

	local_runing = True
	while local_runing:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.unicode == 'n':
					local_runing = False
					# print('test_wait done')
					return 0


def displayScreenSaver():

	SSruning = True
	while SSruning:
		screen.blit(pygame.transform.scale(load_image('screen_saver_start.jpg'), (600, 600)), (0, 0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == 13:
					SSruning = False
		pygame.display.flip()

def displayEnding():
	SSruning = True
	pygame.mixer.music.pause()
	ending_music = pygame.mixer.Sound(os.path.join("data", "ending.ogg"))
	ending_music.play()
	while SSruning:
		screen.blit(pygame.transform.scale(load_image('ending.jpg'), (600, 600)), (0, 0))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.KEYDOWN:
				if event.key == 13:
					SSruning = False
		pygame.display.flip()


class StopMovingError(Exception):
	pass


def matrix_max(array):
	return max([max(i) for i in array])


def load_image(name, colorkey=None):
	fullname = os.path.join("data", name)
	try:
		image = pygame.image.load(fullname)
	except pygame.error as message:
		# print("Cannot load the image")
		raise SystemExit(message)
	image = image.convert_alpha()
	if colorkey is not None:
		colorkey = image.get_at((0, 0))
		image.set_colorkey(colorkey)
	return image

def loadAndPlayFM(name):
	fullname = os.path.join("data", name)
	pygame.mixer.music.load(fullname)
	pygame.mixer.music.play(-1)


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
		self.holos_amount = 0
		self.holos = []


	def render(self):
		for i in range(self.x):
			for j in range(self.y):
				pygame.draw.rect(screen, pygame.Color('black'), (self.left + self.cell_size * i, self.top + self.cell_size * j, self.cell_size, self.cell_size), 1)


	def empty(self):
		self.board = [[0] * self.x for i in range(self.y)]
		self.maxnum = 0
		self.blocklist = []
		self.holos_amount = 0
		self.holos = []


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
			if block.number == self.board[cell_coords[1]][cell_coords[0]]:
				needed_block = block
		try:
			a = needed_block
		except Exception:
			# print('Cannot find a block')
			pass
		else:
			return needed_block

	def create_borders():
		vertical_border = pygame.sprite.Sprite()
		vertical_border.image = load_image("vertical.jpg")
		vertical_border.rect = vertical_border.image.get_rect()
		vertical_border.rect.x = 50
		vertical_border.rect.y = 50
		vertical_borders.add(vertical_border)

		vertical_border2 = pygame.sprite.Sprite()
		vertical_border2.image = load_image("vertical1.jpg")
		vertical_border2.rect = vertical_border2.image.get_rect()
		vertical_border2.rect.x = 540
		vertical_border2.rect.y = 50
		vertical_borders.add(vertical_border2)

		vertical_border3 = pygame.sprite.Sprite()
		vertical_border3.image = load_image("vertical2.jpg")
		vertical_border3.rect = vertical_border2.image.get_rect()
		vertical_border3.rect.x = 540
		vertical_border3.rect.y = 300
		vertical_borders.add(vertical_border3)

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


class Block(pygame.sprite.Sprite):

	HORIZONTAL = 0
	VERTICAL = 1
	CUBE = 2

	def __init__(self, x, y, length, board, orientation, holographic = False):
		self.x = x
		self.y = y
		self.holographic = holographic
		self.length = length
		self.board = board
		self.orientation = orientation
		self.number = (self.board.maxnum + 1) if not holographic else (self.board.holos_amount - 2)
		self.board.maxnum += 1 if not holographic else 0
		self.image = None
		self.right_side_x = self.y + self.length * self.board.cell_size
		if self.orientation == Block.HORIZONTAL:
			for i in range(self.length):
				self.board.board[self.y][self.x + i] = self.number
			if self.length == 2:
				self.image = pygame.transform.scale(load_image("horizontal2.png"), (160, 80))
			elif self.length == 3:
				self.image = pygame.transform.scale(load_image("horizontal3.png"), (240, 80))
			if self.x == 0 and self.y == 2:
				self.image = pygame.transform.scale(load_image("main.png"), (160, 80))

		elif self.orientation == Block.VERTICAL:
			for i in range(self.length):
				# print(y + i)
				# print(self.number)
				self.board.board[self.y + i][self.x] = self.number
			if self.length == 3:
				self.image = pygame.transform.scale(load_image("vertical3.png"), (80, 240))
			elif self.length == 2:
				self.image = pygame.transform.scale(load_image("vertical2.png"), (80, 160))
			# self.image = pygame.Surface((self.board.cell_size, self.board.cell_size * self.length))

		elif self.orientation == Block.CUBE:
			for line in range(self.length):
				for row in range(self.length):
					self.board.board[self.y + row][self.x + line] = self.number
			if self.x == 2 and self.y == 3:
				self.image = pygame.transform.scale(load_image("menublock.png"), (80, 80))
			else:
				self.image = pygame.transform.scale(load_image("shina.png"), (80, 80))

		# self.image.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

		pygame.sprite.Sprite.__init__(self)
		self.rect = self.image.get_rect()
		self.rect.x = self.x * self.board.cell_size + self.board.left
		self.rect.y = self.y * self.board.cell_size + self.board.top

		if holographic:
			self.number = self.board.holos_amount - 1
			self.board.holos_amount -= 1
			self.board.holos.append(self)
		self.add_to_group(block_sprites)

	def add_to_group(self, group):
		group.add(self)
		self.board.blocklist.append(self)

	def move(self, delta, dir = None):
		if self.orientation == Block.HORIZONTAL:
			self.rect.x += delta[0]

		elif self.orientation == Block.VERTICAL:
			self.rect.y += delta[1]

		elif self.orientation == Block.CUBE:
			self.rect.x += delta[0]
			self.rect.y += delta[1]

	def update(self, delta):
		try:
			self.move(delta)
			if pygame.sprite.spritecollideany(self, horizontal_borders):
				delta = -1 * delta[0], -1 * delta[1]
				raise StopMovingError

			if pygame.sprite.spritecollideany(self, vertical_borders):
				delta = -1 * delta[0], -1 * delta[1]
				raise StopMovingError

			for i in self.board.holos:
				block_sprites.remove(i)
			block_sprites.remove(self)

			if pygame.sprite.spritecollideany(self, block_sprites):
				for i in self.board.holos:
					block_sprites.add(i)
				block_sprites.add(self)
				delta = -1 * delta[0], -1 * delta[1]
				raise StopMovingError

			for i in self.board.holos:
				block_sprites.add(i)
			block_sprites.add(self)
			self.count_right_side_x()

		except StopMovingError:
			self.update(delta)

	def finish_moving(self):
		if self.rect.x >= self.board.left + self.board.cell_size * (self.board.x - (self.length if self.orientation == Block.HORIZONTAL or self.orientation == Block.CUBE else 0)):
			self.rect.x = self.board.left + self.board.cell_size * (self.board.x - (self.length if self.orientation == Block.HORIZONTAL or self.orientation == Block.CUBE else 0))

		if self.rect.y >= self.board.top + self.board.cell_size * (self.board.y - (self.length if self.orientation == Block.VERTICAL or self.orientation == Block.CUBE else 0)):
			# print("self.rect.y = {}".format(self.rect.y))
			self.rect.y = self.board.top + self.board.cell_size * (self.board.y - (self.length if self.orientation == Block.VERTICAL or self.orientation == Block.CUBE else 0))
			# print("self.rect.y = {}".format(self.rect.y))

		self.rect.x = self.rect.x // self.board.cell_size * self.board.cell_size + self.board.left
		# print("self.rect.y = {}".format(self.rect.y))
		self.rect.y = self.rect.y // self.board.cell_size * self.board.cell_size + self.board.top
		# print("self.rect.y = {}".format(self.rect.y))
		self.x = (self.rect.x - self.board.left) // self.board.cell_size
		self.y = (self.rect.y - self.board.top) // self.board.cell_size

		
		new_board = [[0] * self.board.x for i in range(self.board.y)]
		for i in range(len(self.board.board)):
			for item in range(len(self.board.board[i])):
				if self.board.board[i][item] != self.number:
					new_board[i][item] = self.board.board[i][item]
		self.board.board = new_board

		# test_wait()
		# print('test_wait 1')
		# print('self.orientation = {}'.format(self.orientation))

		if self.orientation == Block.HORIZONTAL:
			# print('i`m here')
			for i in range(self.length):
				self.board.board[self.y][self.x + i] = self.number

		elif self.orientation == Block.VERTICAL:
			for i in range(self.length):
				self.board.board[self.y + i][self.x] = self.number


		elif self.orientation == Block.CUBE:
			for line in range(self.length):
				for row in range(self.length):
					self.board.board[self.y + row][self.x + line] = self.number
		# test_wait()
		# print('test_wait 2')
		click.play()


	def get_covered(self):
		block_sprites.remove(self)
		a = pygame.sprite.spritecollideany(self, block_sprites)
		block_sprites.add(self)
		return a

	def set_text(self, text, size = 20):
		self.text = text.split("\n")
		fonts = []
		myfont = pygame.font.SysFont("comicsansms", size)
		merged_text = self.image
		for i in range(len(self.text)):
			text_line = myfont.render(self.text[i], True, (255, 255, 255))
			merged_text.blit(text_line, (self.image.get_rect().centerx - text_line.get_rect().centerx, size * i))
		self.image = merged_text

	def get_info(self):
		infos = []
		infos.append("Block")
		infos.append("self.number " + str(self.number))
		infos.append("self.orientation " + str(self.orientation))
		infos.append("self.length " + str(self.length))
		infos.append("self.x, self.y = " + str(self.x) + ' ' + str(self.y))
		infos.append('\n')
		return '\n'.join(infos)

	def count_right_side_x(self):
		# print("counted")
		if self.orientation == MenuBlock.HORIZONTAL:
			self.right_side_x = self.rect.x + self.length * self.board.cell_size
		elif self.orientation == MenuBlock.VERTICAL:
			self.right_side_x = self.rect.x + self.board.cell_size

		# print(self.right_side_x)

class MenuBlock(Block):

	HORIZONTAL = 0
	VERTICAL = 1

	def __init__(self, board):
		self.x = 2
		self.y = 3
		self.length = 2
		self.board = board
		self.orientation = MenuBlock.CUBE
		self.number = self.board.maxnum + 1
		self.board.maxnum += 1
		if self.orientation == MenuBlock.HORIZONTAL:
			for i in range(self.length):
				self.board.board[self.y][self.x + i] = self.number

		elif self.orientation == MenuBlock.VERTICAL:
			for i in range(self.length):
				self.board.board[self.y + i][self.x] = self.number

		elif self.orientation == Block.CUBE:
			for line in range(self.length):
				for row in range(self.length):
					self.board.board[self.y + row][self.x + line] = self.number
			self.image = pygame.Surface(
				(self.board.cell_size * self.length, self.board.cell_size * self.length))

		pygame.sprite.Sprite.__init__(self)
		self.image = load_image('menu_brick_texture.jpg')
		self.rect = self.image.get_rect()
		self.rect.x = self.x * self.board.cell_size + self.board.left
		self.rect.y = self.y * self.board.cell_size + self.board.top
		self.add_to_group(block_sprites)

	def __str__(self):
		return str(self.number) + 'MENU BLOCK'


class Handler():

	def load_menu(board, state = 0):
		block_sprites.empty()
		board.empty()
		block = Block(0, 0, 1, board, Block.CUBE, True)
		block.set_text("\n1")
		block = Block(1, 0, 1, board, Block.CUBE, True)
		block.set_text("\n2")
		block = Block(2, 0, 1, board, Block.CUBE, True)
		block.set_text('\n3')
		block = Block(3, 0, 1, board, Block.CUBE, True)
		block.set_text('\n4')
		block = Block(4, 0, 1, board, Block.CUBE, True)
		block.set_text('\n5')
		block = Block(5, 0, 1, board, Block.CUBE, True)
		block.set_text('\n6')
		menublock = Block(2, 3, 1, board, Block.CUBE)
		# menublock.set_text("Put me\nOn\nLVL")


	def loadLevel(level_number, board):
		global MENUISON
		filename = 'levels.json'
		with open(filename) as file:
			levels = json.loads(file.read())
		level = levels[str(level_number)]
		board.empty()
		block_sprites.empty()
		"""
		for col in range(len(board.board)):
			for row in range(len(board.board[col])):
				if type(level[row][col]) == str:
					print("level[row][col] = {}, row = {}, col = {}".format(level[row][col], row, col))
					inf = level[row][col].split()
					block = Block(row, col, int(inf[2]), board, int(inf[1]))
					test_wait()
		MENUISON = False
		"""
		for col in range(len(level)):
			for row in range(len(level[col])):
				if type(level[col][row]) == str:
					# print("level[row][col] = {}, row = {}, col = {}".format(level[row][col], row, col))
					inf = level[col][row].split()
					block = Block(col, row, int(inf[2]), board, int(inf[1]))
					# print(block.get_info())
					# test_wait()
		# print("\n".join([str(i) for i in board.board]))
		# MENUISON = False

loadAndPlayFM('can`t stand it.mp3')
displayScreenSaver()


background_image = load_image('background_image.jpg')
running = True
block_sprites = pygame.sprite.Group()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
Board.create_borders()

current_level = 1
# loadLevel(1)

board = Board(6, 6, 60, 60, 80)
# menublock = MenuBlock(board)
menublock = Block(2, 3, 1, board, Block.CUBE)
menublock.set_text("Put me\nOn\nLVL")
Handler.load_menu(board)
clock = pygame.time.Clock()
fps = 60

moving = 0
brick = None
MENU = 0
level = MENU
MENUISON = True
current_level = 0
# h.load_menu("")

while running:
	screen.blit(background_image, (0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.pos[0] in range(60, 541) and event.pos[1] in range(60, 541):
				cell = board.get_cell(event.pos)
				brick = board.get_brick(cell, event.pos)
				if brick is not None and not brick.holographic:
					moving = brick.number
				else:
					moving = 0
				LP = event.pos

		elif event.type == pygame.MOUSEBUTTONUP:
			moving = 0
			try:
				if brick is not None and not brick.holographic:
					brick.finish_moving()
					covered = brick.get_covered()
					if covered and MENUISON:
						# print(covered.number)
						current_level = covered.number * -1
						Handler.loadLevel(covered.number * -1, board)
					# brick.finish_moving()
					# test_wait()

					# brick.finish_moving()
				brick = None
			except NameError:
				pass

		elif event.type == pygame.MOUSEMOTION:
			try:
				if brick is not None and not brick.holographic:
					# print('жжъьжъьжьъь')
					delta = event.pos[0] - LP[0], event.pos[1] - LP[1]
					LP = event.pos
					brick.update(delta)
					if brick.right_side_x > 550:
						brick.finish_moving()
						clock.tick(1)
						current_level += 1
						if current_level > 6:
							displayEnding()
						else:
							Handler.loadLevel(current_level, board)
							level_winner.play()
						del brick
			except NameError:
				pass
					

		# elif event.type == pygame.KEYDOWN:
			# if event.unicode == 'b':
				# print("\n".join([str(i) for i in board.board]))
			# if event.unicode == 'v':
				# print(brick.right_side_x)
			
			"""
			if event.unicode == 'e':
				displayEnding()
				Handler.load_menu(board)
			"""

	
	"""
	if menublock.x == 3 and menublock.y == 3 and level == MENU:
		Handler.loadLevel(current_level, board)
		level = current_level
	"""

	board.render()
	block_sprites.draw(screen)
	vertical_borders.draw(screen)
	horizontal_borders.draw(screen)
	pygame.display.flip()
	clock.tick(fps)

pygame.quit()
sys.exit()