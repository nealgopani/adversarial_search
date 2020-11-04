from mesa import Agent, Model
from mesa.time import BaseScheduler
import matplotlib.pyplot as plt
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
import math
from collections import OrderedDict 
import asyncio

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

#set to load from file

d = 12

class Pit(Agent):
	def __init__(self, name, model):
		super().__init__(name, model)
		self.name = name

		#cost calculated based on position of agent on the grid
		self.color = 'black'

	def is_diagnal(self, pos1, pos2):
		directions = [(1,1), (1,-1), (-1, 1), (-1, -1)]
		for d in directions:
			if pos2 == tuple(map(sum,zip(pos1,d))):
				return True


class Piece(Agent):
	def __init__(self, name, model, player):
		super().__init__(name, model)
		self.name = name
		self.player = player #will be either adversary or agent
		self.piece_to_image = {'wumpus': 'wumpus.jpg', 'hero': 'hero.png', 'mage': 'mage.png'}
		self.img = self.piece_to_image[name]


	def is_diagnal(self, pos1, pos2):
		directions = [(1,1), (1,-1), (-1, 1), (-1, -1)]
		for d in directions:
			if pos2 == tuple(map(sum,zip(pos1,d))):
				return True

	def _calculate_distance(self, pos1, pos2):
		x1, y1 = pos1 
		x2, y2 = pos2 
		dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		return dist 


	def step(self):
		self.move()


	def move(self):
		if self.player == 'adversary':
			'''
			what we will do is get the neighborhood of the piece

			'''
			neighbors = self.model.grid.get_neighborhood(self.pos, moore = True, include_center = False, radius = 1)
			print('possible positions are: ')
			for n in neighbors:
				print(n)

			print(f'Move {self.name} to: ', end='')
			pos = input()
			pos = pos.split()

			x, y = int(pos[0]), int(pos[1])
			self.model.grid.move_agent(self, (x, y))
			print('Done')

		


class GridModel(Model):
	def __init__(self, width, height):
		self.running = True
		self.grid = MultiGrid(width, height, False) #true for toroidal grid
		self.schedule = BaseScheduler(self)
	# Create agents

		self.initialize_grid()
		self.start = (1,1)


	
	def _calculate_distance(self, pos1, pos2):
		x1, y1 = pos1 
		x2, y2 = pos2 
		dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		return dist 

	
	def initialize_grid(self):
		#initialize the pits
		num_pits = (d//3) - 1
		for j in range(1, d - 1):
			for i in random.sample(list(range(0, d)), d)[0:num_pits]:
				pit = Pit('pit', self)
				self.grid.place_agent(pit, (i, j))


		#init all pieces
		num_pieces = d//3
		for j in range(d):
			j_off = j + 1
			if j_off % 3 == 1:
				piece_adv = Piece('wumpus', self, 'adversary')
				piece_agent = Piece('wumpus', self, 'agent')
			elif j_off % 3 == 2:
				piece_adv = Piece('hero', self, 'adversary')
				piece_agent = Piece('hero', self, 'agent')
			else:
				piece_adv = Piece('mage', self, 'adversary')
				piece_agent = Piece('mage', self, 'agent')

			self.grid.place_agent(piece_adv, (j, 0))
			self.grid.place_agent(piece_agent, (j, d-1))


	def get_position(self):
		agents = []
		pos = ''
		while pos.split() == None or len(pos.split()) != 2 or agents == [] or agents[0].name == 'pit' or agents[0].player == 'agent':

			print("Enter position of piece you want to move (sep by spaces): ", end ='')
			pos = input()
			coord = pos.split()

			if len(pos.split()) != 2:
				print('Entered too little or too many arguments')
				continue
			try:
				x, y = int(coord[0]), int(coord[1])
			except:
				agents = []
				continue

			if x not in range(d) or y not in range(d):
				print('out of bounds')
				agents = []
				continue
			agents = list(self.grid[x][y])
			if agents != [] and agents[0].name != 'pit' and agents[0].player == 'adversary':
				piece = agents[0]
				return piece

			else:
				if agents != [] and agents[0].player == 'agent':
					print('You cannot move agent\'s pieces')
				else:
					print('You have selected either an empty grid or pit')
				continue

	
	def step(self):
		piece = self.get_position()
		self.schedule.add(piece)
		self.schedule.step()
		self.schedule.remove(piece)


if __name__ == '__main__':
	model = GridModel(d, d)
	for i in range(10):
		model.step()

