def manhattan_distance(board):
	return board.evaluate()

def num_remaining_pieces(board):
	return len(board.agent_pieces) - len(board.adversary_pieces)


def num_threats(board):
	'''
	This evaluates how many threats surround each of the agent's pieces in a radius of d/3
	'''
	d = board.grid.width
	radius = d//3
	n_threats = 0
	for agent in board.agent_pieces:
		neighborhood = agent.get_valid_positions(r = radius)
		for n in neighborhood:
			x,y = n
			occupants = list(board.grid[x][y])
			if occupants != []:
				if occupants[0].name == 'pit':
					n_threats += 1
				elif occupants[0].player != agent.player:
					n_threats += 1
	return -n_threats


def distance_to_middle(board):
	'''
	Evaluates average distance of adversary pieces to middle of board - average distance of agent pieces to middle of board
	if agent is closer to the middle, this is an advantageous position.
	'''
	d = board.grid.width
	#if d is even, then we use (d-1)//2 and d//2
	if d % 2 != 0:
		middle = d // 2
		agent_distance = 0
		for agent in board.agent_pieces:
			_, y = agent.pos 
			agent_distance += abs(y - middle)

		adv_distance = 0
		for adv in board.adversary_pieces:
			_, y = adv.pos 
			adv_distance += abs(y - middle)

		return adv_distance - agent_distance 
	else:
		middle_agent = (d - 1) // 2
		middle_adv = d  // 2
		agent_distance = 0
		for agent in board.agent_pieces:
			_, y = agent.pos 
			agent_distance += abs(y - middle_agent)

		adv_distance = 0
		for adv in board.adversary_pieces:
			_, y = adv.pos 
			adv_distance += abs(y - middle_adv)

		return adv_distance - agent_distance 


def num_available_moves(board):
	#evaluates number of available moves of each piece
	n_moves = 0
	for agent in board.agent_pieces:
		neighborhood = agent.get_valid_positions()
		n_moves += len(neighborhood)

	return n_moves