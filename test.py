# -*- coding: utf-8 -*-

import json

class Handler():

	def load_menu(board, state = 0):
		block_sprites.empty()
		board.empty()
		block = Block(0, 0, 1, board, Block.CUBE, True)
		block.set_text("\nLevel\n1")
		block = Block(1, 0, 1, board, Block.CUBE, True)
		block.set_text("\nLevel\n2")
		block = Block(2, 0, 1, board, Block.CUBE, True)
		block.set_text("\nLevel\n3")
		menublock = Block(2, 3, 1, board, Block.CUBE)
		menublock.set_text("Put me\nOn\nLVL")


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
		MENUISON = False
		"""
		for col in range(len(levels)):
			for row in range(len(levels[col])):
				if type(level[row][col]) == str:
					print("level[row][col] = {}, row = {}, col = {}".format(level[row][col], row, col))
					inf = level[row][col].split()
					block = Block(row, col, int(inf[2]), board, int(inf[1]))
		MENUISON = False


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
			print('Cannot find a block')
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


board = Board(6, 6, 60, 60, 80)
Handler.loadLevel(1, board)