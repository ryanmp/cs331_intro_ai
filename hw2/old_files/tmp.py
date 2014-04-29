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





# game tree object
# basic Node class... used to create tree srtucture
class Node(object):
	def __init__(self, data, parent=None):
		self.data = data
		self.children = []
		self.parent = parent
		self.depth = 0
		self.x_wins = 0
		self.o_wins = 0
		self.ties = 0
		self.whose_turn = 0
		self.val = None

	def add_child(self, obj):
		self.children.append(obj)
		#the last child is the one just added
		self.children[-1].parent = self

	def return_leaves(self):
		leaves=[]
		def inner(self,leaves):
			next = self.children
			if next:
				for i in next:
					#leaves.append(inner(i,leaves))
					inner(i,leaves)
			else:
				leaves.append(self)
		inner(self,leaves)
		return leaves

	'''
	def eval_bottom_up(self):
		print "running eval on tree..."

		# oops... forgot to include whose_turn
		self.whose_turn = 1
		whose_turn = -1
		# set whose_turn variable
		def inner(self,whose_turn):
			next = self.children
			this_turn = whose_turn
			next_turn = whose_turn * -1
			if next:
				for i in next:
					i.whose_turn = this_turn
					inner(i,next_turn)
		inner(self,whose_turn)

		l = self.return_leaves()
		for i in l:
			def inner(i):
				if (i.parent): #not root


					# if whose_turn == 1:
					# 	if i.x
					# 	if i.ties > 0: i.parent.ties = 1
					# if whose_turn == -1:
					# 	if i.o_wins > 0:
					# 		i.parent.o_wins = 1
					# 		i.parent.x_wins = 0
					# 	if i.ties > 0: i.parent.ties = 1


					if whose_turn == 1:
						if i.val == 10: i.parent.val = 10
					if whose_turn == -1:
						if i.val == -10:
							i.parent.val = -10


					inner(i.parent)
			inner(i)
		'''





def get_best_move2(self,which_player):

	print "get best move - who?", which_player

	min_ratio = sys.maxint
	max_ratio = 0

	min_x_wins = sys.maxint

	idx = 0

	for i in xrange(len(self.children)):

		o = self.children[i].o_wins
		x = self.children[i].x_wins

		if (x==0): x = .1
		if (o==0): o = .1

		if (which_player == -1):
			if x < min_x_wins:
				min_x_wins = x
				idx = i
		elif (which_player == 1):
			r = o/x
			if r < min_ratio:
				min_ratio = r
				idx = i
	return self.children[idx]


def get_best_move(self,which_player):

	maximize = -1
	minimize = sys.maxint
	pick = self.children[0]

	for idx in xrange(len(self.children)):
		i = self.children[idx]
		print idx, i.val

		if (which_player == 1): #x
			if i.val >= maximize:
				maximize = i.val
				pick = self.children[idx]

		if (which_player == -1): #0
			if i.val <= minimize:
				minimize = i.val
				pick = self.children[idx]


	return pick




def generate_game_tree():
	print 'generating game tree'

	s1 = game([[0,0,0],[0,0,0],[0,0,0]])
	whose_turn = 1
	root = Node(s1)

	def recursive(root,s1,whose_turn):

		to_add = s1.get_successors(whose_turn)

		#print len(to_add)

		this_turn = whose_turn
		next_turn = whose_turn * -1

		for i in to_add:

			new_node = Node(i)
			root.add_child(new_node)

			t1 = i.get_num_open_squares()
			t2 = i.check_for_win()
			if (t1 <= 0):
				#new_node.ties = 1
				new_node.val = 0
				return 0
			if (t2 == 1):
				#new_node.x_wins = 10
				new_node.val = 10
				return 10
			if (t2 == -1):
				#new_node.o_wins = 10
				new_node.val = -10
				return -10

			#print '.b', root.val


			tmp = recursive(new_node, i, next_turn)

			if (tmp != None):

				if (this_turn == 1):
					root.val = max(tmp, root.val)
					#return root.val


				if (this_turn == -1):
					root.val = min(tmp, root.val)
					#return root.val




	recursive(root, s1,whose_turn) #takes a couple of minutes to calculate
	#root.print_tree() #and a couple of minutes to print
	print 'done'

	return root




def move(g,_type,whose_turn,game_tree_node):


	if (whose_turn == 1):
		print "x to move..."
	else:
		print "o to move..."


	if (_type=='random'):
		g.random_play(whose_turn)

	elif (_type=='human'):
		while (True):
			idx = int( raw_input('enter a move (0-8): ') )
			new_play = [[0,0,0],[0,0,0],[0,0,0]]
			xx = int(idx/3) ; yy = idx%3
			if (xx,yy) in g.get_open_squares(): break;

		new_play[xx][yy] = whose_turn
		g.play(new_play)

	elif(_type == 'minimax'):
		l = get_best_move(game_tree_node, whose_turn)
		g.data = l.data.data

	else: # override
		new_play = [[0,0,0],[0,0,0],[0,0,0]]
		xx = _type[0] ; yy = _type[1]
		new_play[xx][yy] = whose_turn
		g.play(new_play)

	# update position in tree
	for i in game_tree_node.children:
		if ((i.data.data==g.data).all()):
			game_tree_node = i

	g.print_state()
	return g, game_tree_node



def play_game(type1,type2):

	# initialize board
	s1 = game([[0,0,0],[0,0,0],[0,0,0]])
	s1.print_state()

	whose_turn = 1 	# x always goes first

	current_node = t

	while (True):

		# x move!
		s1, current_node = move(s1,type1,whose_turn, current_node)
		whose_turn *= -1

		winner = s1.check_for_win()
		if (winner == 1):
			print "x wins"
			break
		elif (winner == -1):
			print "o wins"
			break
		if (s1.get_num_open_squares() <= 0):
			print "tie"
			break

		# o move!
		s1, current_node = move(s1,type2,whose_turn, current_node)
		whose_turn *= -1

		winner = s1.check_for_win()
		if (winner == 1):
			print "x wins"
			break
		elif (winner == -1):
			print "o wins"
			break
		if (s1.get_num_open_squares() <= 0):
			print "tie"
			break


def main(argv):


	try:
		print "loading gametree into mem (could take 30 seconds)"
		t = pickle.load( open( "tree.p", "rb" ) ) #load
	except:
		print "couldn't find saved game tree..."
		to_dump = generate_game_tree()
		to_dump.eval_bottom_up()
		pickle.dump( to_dump, open( "tree.p", "wb" ) ) #save
		t = to_dump
	current_node = t


	if (len(argv) != 2):
		print "Needs 2 args."
		print "They can be: 'human', 'random', or 'minimax'."
		return 0

	print "starting "+ str(argv[0]) +" vs. "+ str(argv[1]) +" game..."

	play_game(argv[0],argv[1])




argv = ["",""]
argv[0] = "minimax"
argv[1] = "minimax"



try:
	print "loading gametree into mem (could take 30 seconds)"
	t = pickle.load( open( "tree.p", "rb" ) ) #load
except:
	print "couldn't find saved game tree..."
	to_dump = generate_game_tree()
	#to_dump.eval_bottom_up()
	#pickle.dump( to_dump, open( "tree.p", "wb" ) ) #save
	t = to_dump
current_node = t


os.system('say "done"')

print "starting "+ str(argv[0]) +" vs. "+ str(argv[1]) +" game..."

play_game(argv[0],argv[1])


#if __name__ == "__main__":
	#ret = main(sys.argv[1:])
