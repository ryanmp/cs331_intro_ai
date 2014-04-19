import sys, time

'''

Ryan Phillips
April 18th, 2014
CS331 - A.I.
Assignment One

Description: 8-tile puzzle solver

To run:
	python hw1.py
	< initial puzzle state file >
	< goal puzzle state file >
	< mode >
	< output file >

modes:
	bfs
	dfs 
	iddfs
	astar 

See testGoal1.txt for expected input format

'''

# basic Node class... used to create tree srtucture
class Node(object):
	def __init__(self, data, parent=None):
		self.data = data
		self.children = []
		self.parent = parent
		# to be set via heuristic f() in astar
		# (not the cleanest solution, but it'll work for now)
		self.h = 0 
		# to be set for iddfs
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
			print idx; print self.depth; print_state(self.data)
			for i in self.children:
				i.print_tree(idx)
	# travels up the tree from leaf to root
	def print_solution(self, leaf):
		ret = []
		def inner(leaf):
			ret.append(leaf.data)
			if (leaf.parent):
				inner(leaf.parent)
		inner(leaf)
		ret.reverse()
		return ret

# testGoalX.txt -> python 2d array
def parse_input(file_name):
	f = open(file_name)
	lines_raw = f.readlines()
	ret = [] # file to list of lists
	for i in range(0,len(lines_raw)):
		parsing_line = []
		parsing_line = lines_raw[i].split(',')
		parsing_line = map(int, parsing_line)
		ret.append(parsing_line)
	return ret

# a slightly cleaner print for our arrays
def print_state(state):
	for i in xrange(3):
		print(state[i])
	print ""

def get_possible_swaps(state):
	swaps = [1,1,1,1] # North, E, S, W
	idx = get_idx(state,0)
	if idx[0] == 0:
		swaps[0] = 0
	if idx[1] == 2:
		swaps[1] = 0
	if idx[0] == 2:
		swaps[2] = 0
	if idx[1] == 0:
		swaps[3] = 0
	return swaps

def is_solution(current_state, goal_state):
	ret = True;
	for i in xrange(3):
		for j in xrange(3):
			if current_state[i][j] != goal_state[i][j]:
				ret = False
	return ret

def do_swap(state, which): #which: 0-3
	new_state = [[i for i in j] for j in state]
	t = get_idx(new_state,0)
	if which == 0:
		t2 = (t[0]-1,t[1])
	elif which == 1:
		t2 = (t[0],t[1]+1)
	elif which == 2:
		t2 = (t[0]+1,t[1])
	elif which == 3:
		t2 = (t[0],t[1]-1)
	else: sys.exit("error")
	temp = new_state[t[0]][t[1]]
	new_state[t[0]][t[1]] = new_state[t2[0]][t2[1]]
	new_state[t2[0]][t2[1]] = temp
	return new_state

# helper function, used by do_swap
def get_idx(state,num):
	ret = (0,0)
	for i in xrange(len(state)):
		for j in xrange(len(state[i])):
			if state[i][j] == 0:
				ret = (i,j)
	return ret

# this new version uses the tree properly now 
def get_succ(node):
	state = node.data
	ret = [] 
	swaps = get_possible_swaps(state)
	for i in xrange(len(swaps)):
		if swaps[i] == 1:
			new_state = do_swap(state,i)
			new_node = Node(new_state)
			node.add_child(new_node)
			ret.append(new_node)
	return ret, node

# basic breadth-first search
def bfs(s0,s1):
	frontier = []
	explored = []
	root = Node(s0)
	to_add, tree = get_succ(root)
	for i in to_add: frontier.append(i)
	x = 0
	while(x < 1000): #some max bound just in case
		x+=1
		if (len(frontier) <= 0): return False, "fail0"
		leaf = frontier.pop(0) 
		if is_solution(leaf.data, s1): 
			return True, (root, leaf, x)
			#root.print_solution(leaf)
		explored.append(leaf)
		to_add, tree = get_succ(leaf)
		for i in to_add:
			if i not in frontier:
				if i not in explored:
					frontier.append(i)
	return False, "fail1 - exceeded max iterations of: "+str(x)

# depth-first search
# the only differences between this and bfs is in the frontier.pop()
# note: dfs seems to be an awful method for this search space...
# even after expanding 10,000 nodes it still hasn't found the sol yet.
# If I optimized my code, it would eventually find the solution prior to hitting
# 9! nodes, but I don't have the patience for that at the moment
def dfs(s0,s1):
	frontier = []
	explored = []
	root = Node(s0)
	to_add, tree = get_succ(root)
	for i in to_add: frontier.append(i)
	x = 0
	while(x < 500): # max bound
		x+=1
		if (len(frontier) <= 0): return False, "fail0"
		leaf = frontier.pop() 
		if is_solution(leaf.data, s1): 
			return True, (root, leaf, x)
			#root.print_solution(leaf)
		explored.append(leaf)
		to_add, tree = get_succ(leaf)
		for i in to_add:
			if i not in frontier:
				if i not in explored:
					frontier.append(i)
	return False, "fail1 - exceeded max iterations of: "+str(x)


# this new version uses the tree properly now 
def get_succ_id(node,root):
	state = node.data
	ret = [] 
	swaps = get_possible_swaps(state)
	for i in xrange(len(swaps)):
		if swaps[i] == 1:
			new_state = do_swap(state,i)
			new_node = Node(new_state)
			node.add_child_set_depth(new_node,root)
			ret.append(new_node)
	return ret, node


# okay, this is not doing iddfs correctly... so this is basically just a placerholder method
# I'll get it straightened out if I have time
def iddfs(s0,s1):
	
	max_depth = 200; current_depth = 0
	while current_depth < max_depth:

		frontier = []
		explored = []
		root = Node(s0)
		to_add, tree = get_succ_id(root,root)
		for i in to_add: frontier.append(i)

		while(len(frontier) > 0): # max bound

			leaf = frontier.pop() 

			if is_solution(leaf.data, s1):


				return True, (root, leaf, len(explored)+1)
				#root.print_solution(leaf)
			explored.append(leaf)
			to_add, tree = get_succ_id(leaf,root)
			for i in to_add:
				if i not in frontier:
					if i not in explored:
						if i.depth < current_depth:
							frontier.append(i)

		current_depth += 1

	return False, "fail1 - exceeded max iterations of: "+str(max_depth)

# a-star search
# uses a_star_h() as the heuristic
def astar(s0,s1):
	frontier = []
	explored = []
	root = Node(s0)
	#root.h = astar_h(root.data,s1)
	to_add, tree = get_succ_astar(root,s1)
	for i in to_add: frontier.append(i)
	x = 0
	while(x < 20): #some max bound just in case
		x+=1
		if (len(frontier) <= 0): return False, "fail0"
		max_h = 0;
		idx = 0
		for i in xrange(len(frontier)):
			if frontier[i].h > max_h:
				idx = i; max_h = frontier[i].h
		leaf = frontier.pop(idx) 
		if is_solution(leaf.data, s1): 
			return True, (root, leaf, x)
		explored.append(leaf)
		to_add, tree = get_succ_astar(leaf,s1)
		for i in to_add:
			if i not in frontier:
				if i not in explored:
					frontier.append(i)
	return False, "fail1 - exceeded max iterations of: "+str(x)

# made a separate version for get_successor, since we are calculating some
# additional information for each node added to the tree
def get_succ_astar(node,s1):
	state = node.data
	ret = [] 
	swaps = get_possible_swaps(state)
	for i in xrange(len(swaps)):
		if swaps[i] == 1:
			new_state = do_swap(state,i)
			new_node = Node(new_state)
			new_node.h = astar_h(new_node.data,s1)
			node.add_child(new_node)
			ret.append(new_node)
	return ret, node

# just counts the number of matches
def astar_h(s0,s1):
	matches = 0
	for i in xrange(3):
		for j in xrange(3):
			if s0[i][j] == s1[i][j]: matches += 1
	return matches		

def format_output(arr):
	ret = "length of solution path: "+ str(len(arr)) + "\n\n"
	ret += "solution: \n"
	# the commented-out code matches that of the input files,
	# but I think the print_state arrays look nicer
	'''
	for i in arr:
		for j in xrange(3):
			for k in xrange(3):
				ret += str(i[j][k])
				if (k!=2): ret += ","
			ret += "\n"
		ret += "\n"
	'''
	for i in arr:
		for j in xrange(3):
			ret += str(i[j])
			ret += "\n"
		ret += "\n"
	return ret

def main(argv):

	if (len(argv) == 0):
		print "needs some args!"
		return 0 

	init_state = parse_input(argv[0])
	goal_state = parse_input(argv[1])
	print "init state"
	print_state(init_state)
	print "goal state"
	print_state(goal_state)

	solution = []

	which = argv[2]
	print "running: ",which,"\n"
	start_time = time.time()
	if (which == 'bfs'):
		solution = bfs(init_state,goal_state)
	elif (which == 'dfs'):
		solution = dfs(init_state,goal_state)
	elif (which == 'iddfs'):
		solution = iddfs(init_state,goal_state)
	elif (which == 'astar'):
		solution = astar(init_state,goal_state)
	else:
		print "unknown command:", which
		print "exiting..."
		sys.exit()

	
	if solution:
		time_elapsed = time.time() - start_time
		to_out = ""
		if solution[0]:
			r = solution[1][0]
			l = solution[1][1]
			as_an_array = r.print_solution(l)
			to_out = format_output(as_an_array)
			to_out = "run time: " + str('%.2E' % time_elapsed) + "\n" + to_out
			to_out = "expanded nodes: " + str(solution[1][2]-1) + "\n" + to_out
			print to_out
		else:
			# failed to find a solution, printing failure info to output
			print solution[1] 
			to_out = solution[1]

		output = open(argv[3], 'w+') 
		output.write(to_out)
		output.close()

if __name__ == "__main__":
   main(sys.argv[1:])



