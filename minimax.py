from copy import deepcopy


def minimax(board, depth, alpha, beta, max_player):
	if depth == 0  or board.winner():
		return board.evaluate(), board, None, None

	if max_player:
		maxEval = float('-inf')
		best_board = None
		b_piece = None
		b_move = None

		for temp_board, piece, move in get_all_moves(board, 'agent'):
			evaluation = minimax(temp_board, depth - 1, alpha, beta, False)[0]

			maxEval = max(maxEval, evaluation)
			alpha = max(evaluation, alpha)
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

		for temp_board, piece, move in get_all_moves(board, 'adversary'):
			evaluation = minimax(temp_board, depth - 1,alpha, beta, True)[0]

			minEval = min(minEval, evaluation)
			beta = min(beta, evaluation)
			if minEval == evaluation:
				best_board = temp_board
				b_piece = piece 
				b_move = move 
			if beta <= alpha:
				break

		return minEval, best_board, b_piece, b_move





def simulate_move(temp_piece, move, temp_board):
	temp_board.grid.move_agent(temp_piece, move)
	temp_board.collision_check(temp_piece)



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