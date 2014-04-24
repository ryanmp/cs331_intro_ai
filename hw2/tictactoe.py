import numpy as np
from sets import Set
import random
import Tkinter as tk
import sys

# uses a 3x3 data array for current state
# 0 for blank
# 1 for x
# -1 for o
class game:
	def __init__(self, data):
		self.data = data
	def print_state(self):
		for i in xrange(3):
			print self.data[i]
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

# game tree object
# basic Node class... used to create tree srtucture
class Node(object):
	def __init__(self, data, parent=None):
		self.data = data
		self.children = []
		self.parent = parent
		self.depth = 0

	def add_child(self, obj):
		self.children.append(obj)
		#the last child is the one just added
		self.children[-1].parent = self

	def add_child_set_depth(self, obj, t):
		#obj.depth = self.depth + 1
		self.children.append(obj)
		self.children[-1].parent = self

		#need to set depth recursively
		def set_depth(t):
			if (t != None or t != str):
				if (len(t.children) > 0):
					for i in t.children:
						if (i != None):
							i.depth = t.depth + 1
							set_depth(i)
		set_depth(t)

	# used primarly for testing purposes
	def print_tree(self, idx=0):
		idx += 1
		if (self):
			print idx; print self.data
			for i in self.children:
				i.print_tree(idx)

#gui stuff
def callback(number):
		print "button", number
		btns[0]["text"] = "ok"

def move(g,type,whose_turn):

	if (type=='random'):
		g.random_play(whose_turn)

	elif (type=='human'):
		while (True):
			idx = int( raw_input('enter a move (0-8): ') )
			new_play = [[0,0,0],[0,0,0],[0,0,0]]
			xx = int(idx/3) ; yy = idx%3
			if (xx,yy) in g.get_open_squares(): break;

		new_play[xx][yy] = whose_turn
		g.play(new_play)

	g.print_state()
	return g


def main(argv):

	# initialize board
	s1 = game([[0,0,0],[0,0,0],[0,0,0]])
	s1.print_state()

	# draw gui stuff
	btns = []
	for i in xrange(3):
		for j in xrange(3):
			temp = tk.Button(text=s1.data[i][j], command=lambda x=i, y=j: callback(x*3+y)).grid(row=i, column=j)
			btns.append(temp)

	if (len(argv) != 2):
		print "Needs 2 args."
		print "They can be: 'human', 'random', or 'minimax'."
		return 0

	print "starting "+ str(argv[0]) +" vs. "+ str(argv[1]) +" game..."

	whose_turn = 1 	# x always goes first

	# game loop
	while (True):

		# x move!
		s1 = move(s1,argv[0],whose_turn)
		whose_turn *= -1

		winner = s1.check_for_win()
		if (winner == -1):
			print "x wins"
			break
		elif (winner == 1):
			print "o wins"
			break
		if (s1.get_num_open_squares() <= 0):
			print "tie"
			break

		# o move!
		s1 = move(s1,argv[1],whose_turn)
		whose_turn *= -1

		winner = s1.check_for_win()
		if (winner == -1):
			print "x wins"
			break
		elif (winner == 1):
			print "o wins"
			break
		if (s1.get_num_open_squares() <= 0):
			print "tie"
			break

		#filename = raw_input('enter a move (0-8): ')

	# gui loop? I still don't know how this is supposed to work
	#tk.mainloop()

if __name__ == "__main__":
	#main(sys.argv[1:])


	'''
	next we are going to compute a complete game tree...
	I know this isn't strictly the minmax AI specificied for this project,
	but it seems like a fun thing to try.
	'''

	print 'generating game tree'
