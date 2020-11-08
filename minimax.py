from copy import deepcopy
import h
from queue import PriorityQueue
import heapq

h_func = h.manhattan_distance

def minimax(board, depth, alpha, beta, max_player):
	if depth == 0  or board.winner():
		return board.evaluate(), board, None, None

	if max_player:
		maxEval = float('-inf')
		best_board = None
		b_piece = None
		b_move = None
		i = 1
		pq = []
		for item in get_all_moves(board, 'agent'):
			temp_board = item[0]
			heuristic = h_func(temp_board)
			a = (-heuristic, i, item)
			heapq.heappush(pq, a)
			i+=1

		while pq != []:
			temp_board, piece, move = heapq.heappop(pq)[2]
			result = minimax(temp_board, depth - 1, alpha, beta, False)
			evaluation = result[0]

			maxEval = max(maxEval, evaluation)
			alpha = max(maxEval, alpha)

			if maxEval == evaluation:				
				best_board = temp_board
				b_piece = piece 
				b_move = move 

			if beta <= alpha:
				break

		return maxEval, best_board, b_piece, b_move
	
	else:
		minEval = float('inf')
		best_board = None
		b_piece = None
		b_move = None

		pq = []
		i = 1
		for item in get_all_moves(board, 'agent'):
			temp_board = item[0]
			heuristic = h_func(temp_board)
			a = (heuristic, i, item)
			heapq.heappush(pq, a)
			i+=1

		while pq != []:
			temp_board, piece, move = heapq.heappop(pq)[2]
			result = minimax(temp_board, depth - 1,alpha, beta, True)
			evaluation = result[0]

			minEval = min(minEval, evaluation)
			beta = min(beta, minEval)

			if minEval == evaluation:
				best_board = temp_board
				b_piece = piece 
				b_move = move 

			if beta <= alpha:
				break



		return minEval, best_board, b_piece, b_move



def simulate_move(temp_piece, move, temp_board):
	temp_board.grid.move_agent(temp_piece, move)
	temp_board.collision_check(temp_piece, not_tree = False)



def get_all_moves(board, player):
	moves = []
	player_pieces = board.adversary_pieces if player == 'adversary' else board.agent_pieces

	for piece in player_pieces:
		valid_moves = piece.get_valid_positions()
		for move in valid_moves:
			temp_board = deepcopy(board)
			x, y = piece.pos 
			temp_piece = list(temp_board.grid[x][y])[0]
			simulate_move(temp_piece, move, temp_board)
			moves.append([temp_board, piece, move])
	return moves