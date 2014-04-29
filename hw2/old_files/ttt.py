# take 2
import numpy as np
from sets import Set
import random
from copy import deepcopy




class Node(object):
	def __init__(self, board, parent=None):
		self.board = board
		self.children = []
		self.parent = parent

	def add_child(self, obj):
		self.children.append(obj)
		#the last child is the one just added
		self.children[-1].parent = self


# none if not finished
# 1 if x wins
# -1 if o wins
# 0 if tie
def check_for_win(gs):
	winning_sets = [Set([0,1,2]),
					Set([3,4,5]),
					Set([6,7,8]),
					Set([0,3,6]),
					Set([1,4,7]),
					Set([2,5,8]),
					Set([0,4,8]),
					Set([2,4,6])]

	for i in winning_sets:
		if i.issubset(gs['x']):
			return 1
		elif i.issubset(gs['o']):
			return -1

	if len(gs['x'] ^ gs['o']) == 9:
		return 0

# returns a set of possible moves
def get_available_moves(gs):
	all_moves = Set([i for i in xrange(9)])
	return all_moves.difference(gs['x'] ^ gs['o'])


def move(gs, move, whose_turn):

		# be careful with this...
		new = deepcopy(gs)

		if (whose_turn == 1):
			new['x'].add(move)
		elif (whose_turn == -1):
			new['o'].add(move)
		else:
			sys.exit('error')

		return new


#print check_for_win(game_state)
#print get_available_moves(game_state)




def run_random_game(gs, whose_turn):
	while (True):

		# first check for win and return if done...
		winner = check_for_win(gs)
		if (winner != None):
			return winner

		# pick a random move for current player
		possible_moves = list(get_available_moves(gs))
		x = random.choice(possible_moves)
		gs = move( gs, x, whose_turn)

		# next player's turn for next iteration
		whose_turn *= -1


# problem,
# modify to use nodes instead of states...
#
def full_game_tree():

	game_state = {'x':Set([]),'o':Set([])}
	game_tree = Node(game_state)
	whose_turn = 1

	def recursive(game_tree, whose_turn):

		# first check for win and return if done...
		winner = check_for_win(game_tree.board)
		if (winner != None):
			return winner

		possible_moves = list(get_available_moves(game_tree.board))
		for i in possible_moves:



			gs = move( game_tree.board, i, whose_turn)
			new_node = Node(gs)
			game_tree.add_child(new_node)

			whose_turn *= -1 # remember the problem with this?
			recursive(new_node, whose_turn)


	recursive(game_tree, whose_turn)

	return game_tree

t = full_game_tree()


#new_node = Node( move(game_state, 0, 1))
#game_tree.add_child(new_node)
