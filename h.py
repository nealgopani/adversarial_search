def manhattan_distance(board):
	return board.evaluate()

def num_of_agent_pieces(board):
	return len(board.agent_pieces) - len(board.adversary_pieces)

