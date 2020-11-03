from mesa import Agent, Model
from mesa.time import RandomActivation
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

d = 9

class Pit(Agent):
	def __init__(self, id, model):
		super().__init__(id, model)

		#cost calculated based on position of agent on the grid
		self.color = 'black'

	def is_diagnal(self, pos1, pos2):
		directions = [(1,1), (1,-1), (-1, 1), (-1, -1)]
		for d in directions:
			if pos2 == tuple(map(sum,zip(pos1,d))):
				return True


class GridAgent(Agent):
	def __init__(self, unique_id, model, start, end):
		super().__init__(unique_id, model)
		self.color = 'orange'
		self.start = start
		self.end = end
		self.cost = None

		self.movements = []

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
		print('Done')

		


class GridModel(Model):
	def __init__(self, width, height):
		self.running = True
		self.grid = MultiGrid(width, height, False) #true for toroidal grid
		self.schedule = RandomActivation(self)
	# Create agents

		self.initialize_grid()
		self.start = (1,1)
		self.agent = GridAgent('Agent', self, (1,1), (2,2))
		self.grid.place_agent(self.agent, self.start)

		self.schedule.add(self.agent)

	
	def _calculate_distance(self, pos1, pos2):
		x1, y1 = pos1 
		x2, y2 = pos2 
		dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
		return dist 

	
	def initialize_grid(self):
		#initialize the pits
		num_pits = (d//3) - 1
		print(num_pits)
		for j in range(1, d - 1):
			for i in random.sample(list(range(0, d - 1)), d-2)[0:num_pits]:
				pit = Pit('pit', self)
				self.grid.place_agent(pit, (i, j))
				print(pit.pos)


		#init all partially blocked cells


		#blocked cell



	
	def step(self):
		self.schedule.step()


if __name__ == '__main__':
	model = GridModel(d, d)
	for i in range(1):
		model.step()

