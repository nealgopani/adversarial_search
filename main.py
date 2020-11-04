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

d = 6 #set this to a multiple of 3 to create a d x d board

def is_valid_position(pos):
	'''
	Makes sure we don't enter letters, an incorrect number of inputs, or an out of bounds position
	'''
	agents = []
	coord = pos.split()
	if not coord or len(coord) != 2:
		return False

	try:
		x, y = int(coord[0]), int(coord[1])
	except:

		return False

	if x not in range(d) or y not in range(d):

		return False

	return True



class Pit(Agent):
	def __init__(self, name, model):
		super().__init__(name, model)
		self.name = name

		#cost calculated based on position of agent on the grid
		self.color = 'black'


class Piece(Agent):
	def __init__(self, name, model, player):
		super().__init__(name, model)
		self.name = name
		self.player = player #will be either adversary or agent
		self.piece_to_image = {'wumpus': 'wumpus.jpg', 'hero': 'hero.png', 'mage': 'mage.png'}
		self.img = self.piece_to_image[name]



	def step(self):
		self.move()

	def get_valid_positions(self):
		#valid neighbors are anything in radius one that does not include one of your own pieces
		neighbors = self.model.grid.get_neighborhood(self.pos, moore = True, include_center = False, radius = 1)
		neighbors_without_own = neighbors[:]


		for n in neighbors:
			x, y = n 
			agents = list(self.model.grid[x][y])
			for a in agents:
				if a.name != 'pit' and a.player == self.player:
					neighbors_without_own.remove(n)
		return neighbors_without_own


	def move(self):
		if self.player == 'adversary':
			'''
			what we will do is get the neighborhood of the piece

			'''
			neighbors = self.get_valid_positions()
			print('possible positions are: ')
			for n in neighbors:
				print(n)

			pos = ''
			while not is_valid_position(pos) or tuple([int(i) for i in pos.split()]) not in neighbors:
				print(f'Move {self.name} to: ', end='')
				pos = input()
			
			pos = pos.split()

			x, y = int(pos[0]), int(pos[1])
			self.model.grid.move_agent(self, (x, y))
			print('Done')
		else:
			# code for moving the agent 
			pass

		


class Board(Model):
	def __init__(self, width, height):
		self.running = True
		self.grid = MultiGrid(width, height, False) #true for toroidal grid
		self.schedule = BaseScheduler(self)


		self.adversary_pieces = []
		self.agent_pieces = []

		self.initialize_grid()

	
	def initialize_grid(self):
		'''
		Here we initialize the d by d board with pits and pieces
		'''

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


	def get_adversary_piece(self):
		'''
		Here is where player enters coordinates of piece they want to move. Checks for invalid inputs and protects
		against them
		'''
		pos = ''
		agents = []

		while not is_valid_position(pos) or agents == [] or agents[0].name == 'pit' or agents[0].player == 'agent' :
			print("Enter position of piece you want to move (sep by spaces): ", end ='')
			pos = input()

			if not is_valid_position(pos):
				print('invalid argument')
				continue

			x, y = int(pos.split()[0]), int(pos.split()[1])

			agents = list(self.grid[x][y])

			if agents != []:
				if agents[0].name == 'pit':
					print('cannot select a pit')
					continue

				if agents[0].player == 'adversary':
					piece = agents[0]
					return piece

				else:
					print('You cannot move agent\'s pieces')
					continue
			else:
				print('cannot select empty square')

	def get_agent_piece_and_move(self):
		'''
		here we will call minimax from minimax.py. This will return the agent piece that will move along with the coordinate
		it will move to
		'''
		pass

	def win(self):
		'''
		here we will implement the winning condition
		we will return the value True and the player who won. we want the game to stop
		when win() == True.. and we will implement this in the step function
		'''

	def collision_check(self, piece):
		x, y = piece.pos 
		agents = list(self.grid[x][y])

		#pop piece from agents
		agents.remove(piece)

		for agent in agents:
			if agent.name == 'pit':
				self.grid.remove_agent(piece)
			elif agent.player != piece.player:
				if agent.name == piece.name:
					self.grid.remove_agent(piece)
					self.grid.remove_agent(agent)
				elif agent.name and piece.name in ['hero', 'wumpus']:
					agent_to_remove = agent if agent.name == 'wumpus' else piece 
					self.grid.remove_agent(agent_to_remove)
				elif piece.name and agent.name in ['mage', 'hero']:
					agent_to_remove = agent if agent.name == 'hero' else piece 
					self.grid.remove_agent(agent_to_remove)
				else:
					agent_to_remove = agent if agent.name == 'mage' else piece 
					self.grid.remove_agent(agent_to_remove)


	
	def step(self):
		'''
		Each time step is called, player enters move and their piece moves. Agent also moves its piece that was returned from
		get_agent_piece_and_move(). This is essentially two turns of the game: player's turn and agent's turn. 

		'''
		adversary_piece = self.get_adversary_piece()
		self.schedule.add(adversary_piece)
		self.schedule.step()
		self.collision_check(adversary_piece)
		self.schedule.remove(adversary_piece)


if __name__ == '__main__':
	model = Board(d, d)
	for i in range(10):
		model.step()
