import numpy as np
from sets import Set
import random
import Tkinter as tk
import sys
import cPickle as pickle
import os

# uses a 3x3 data array for current state
# 0 for blank
# 1 for x
# -1 for o
class game:
	def __init__(self, data):
		self.data = data
	def print_state(self):
		for i in xrange(3):
			s = ""
			for j in xrange(3):
				s+= "|"
				if self.data[i][j] == 1: s+='x'
				if self.data[i][j] == -1: s+='o'
				if self.data[i][j] == 0: s+= ' '
			s+= "|"
			print s
			if i < 2: print "-------"
			#print self.data[i]
		print ""
	# returns 1 of x wins,
	# -1 if 0,
	# 0 if nobody wins
	def check_for_win(self):
		sums = Set()
		temp = np.sum(self.data, axis=0)
		for i in temp: sums.add(i)
		temp = np.sum(self.data, axis=1)
		for i in temp: sums.add(i)

		#don't forget diagonals
		sums.add(self.data[0][0]+self.data[1][1]+self.data[2][2])
		sums.add(self.data[2][0]+self.data[1][1]+self.data[0][2])

		if -3 in sums:
			return -1
		elif 3 in sums:
			return 1
		else:
			return 0

	# error-checks to be sure that this spot is actually empty
	def play(self, this_move):
		# get x,y of this_move
		idx = (0,0)
		for i in xrange(3):
			for j in xrange(3):
				if this_move[i][j] != 0:
					idx = (i,j)
		if (self.data[idx[0]][idx[1]] == 0):
			self.data = np.add(self.data, this_move)
		else:
			print "invalid move!"

	def get_open_squares(self):
		open_squares = []
		for i in xrange(3):
			for j in xrange(3):
				if self.data[i][j] == 0:
					open_squares.append((i,j))
		return open_squares

	def get_num_open_squares(self):
		return len(self.get_open_squares())

	def random_play(self,which_player):
		possible_plays = self.get_open_squares()
		new_play = [[0,0,0],[0,0,0],[0,0,0]]
		x = random.choice(possible_plays)
		new_play[x[0]][x[1]] = which_player
		self.play(new_play)

	def get_successors(self,which_player):
		possible_plays = self.get_open_squares()
		ret = []
		for i in possible_plays:
			temp = game(self.data) #current state of board
			new_play = [[0,0,0],[0,0,0],[0,0,0]]
			new_play[i[0]][i[1]] = which_player
			temp.play(new_play)
			ret.append(temp)
		return ret




# basic Node class... used to create tree srtucture
class Node(object):
	def __init__(self, data, parent=None):
		self.data = data
		self.children = []
		self.parent = parent
		self.val = None

	def add_child(self, obj):
		self.children.append(obj)
		#the last child is the one just added
		self.children[-1].parent = self




def generate_game_tree(s1, whose_turn):
	print 'generating game tree'

	root = Node(s1)

	def minimax(node,whose_turn):

		to_add = node.data.get_successors(whose_turn)
		t1 = node.data.get_num_open_squares()
		t2 = node.data.check_for_win()
		if (t1 <= 0):
			#new_node.ties = 1
			node.val = 0
			return 0
		if (t2 == 1):
			#new_node.x_wins = 10
			node.val = 10
			return 10
		if (t2 == -1):
			#new_node.o_wins = 10
			node.val = -10
			return -10

		if whose_turn == 1:
			bestValue = -1000
			for i in to_add:

				new_node = Node(i)
				node.add_child(new_node)

				val = minimax(new_node, -1)
				bestValue = max(bestValue, val)

			node.val = bestValue
			return bestValue
		elif whose_turn == -1:
			bestValue = 1000
			for i in to_add:

				new_node = Node(i)
				node.add_child(new_node)

				val = minimax(new_node, 1)
				bestValue = min(bestValue, val)

			node.val = bestValue
			return bestValue


	minimax(root, whose_turn)
	print 'done'
	return root





def move(tree,_type,whose_turn):

	ret_node = None


	if (whose_turn == 1):
		print "x to move..."
	else:
		print "o to move..."


	if(_type == 'minimax'):

		#to speed it up, make the first step deterministic
		if tree.data.get_num_open_squares() == 9:
			ret_node = tree.children[0]
		else:

			ret_node = mm_play(tree,whose_turn)

	elif(_type == 'random'):
		ret_node = random.choice(tree.children)

	elif (_type=='human'):
		rang = tree.data.get_num_open_squares()
		while (True):
			idx = int( raw_input('enter a move #: ') )
			if idx >= 0 and idx < rang: break;
		ret_node = tree.children[idx]

	else:
		print "error! invalid player type"


	ret_node.data.print_state()
	return ret_node


def mm_play(t,whose_turn):

	next_node = t.children[0]

	if (whose_turn == 1):
		best = -1000
		for i in xrange(len(t.children)):
			print t.children[i].val
			#best = max(t.children[i].val, best)

			if t.children[i].val > best:
				best = t.children[i].val
				next_node = t.children[i]

		return next_node

	elif (whose_turn == -1):
		best = 1000
		for i in xrange(len(t.children)):
			print t.children[i].val
			#best = min(t.children[i].val, best)

			if t.children[i].val < best:
				best = t.children[i].val
				next_node = t.children[i]

		return next_node



def play_game(type1,type2,t1,whose_turn):



	while (True):

		# x move!
		t1 = move(t1,type1,whose_turn)
		whose_turn *= -1

		winner = t1.data.check_for_win()
		if (winner == 1):
			print "x wins"
			break
		elif (winner == -1):
			print "o wins"
			break
		if (t1.data.get_num_open_squares() <= 0):
			print "tie"
			break

		# o move!
		t1 = move(t1,type2,whose_turn)
		whose_turn *= -1

		winner = t1.data.check_for_win()
		if (winner == 1):
			print "x wins"
			break
		elif (winner == -1):
			print "o wins"
			break
		if (t1.data.get_num_open_squares() <= 0):
			print "tie"
			break



whose_turn = 1
starting_state = game([[0,0,0],[0,0,0],[0,0,0]])
t = generate_game_tree(starting_state, whose_turn)
print "start"
t.data.print_state()

play_game('minimax','minimax',t,whose_turn)
