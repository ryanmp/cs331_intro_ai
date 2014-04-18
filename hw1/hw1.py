import sys

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

class Node(object):
	def __init__(self, data, parent=None):
		self.data = data
		self.children = []
		self.parent = parent
		self.goal = "0"

	def add_child(self, obj):
		self.children.append(obj)
		#the last child is the one just added
		self.children[-1].parent = self 
	def print_tree(self, idx=0):
		idx += 1
		if (self):
			#print self.data, "parent:",self.parent, ",id:",self
			print idx; print_state(self.data)
			for i in self.children:
				i.print_tree(idx)
	def print_solution(self, leaf):
		
		ret = []

		def inner(leaf):
			ret.append(leaf.data)
			if (leaf.parent):
				inner(leaf.parent)
		inner(leaf)

		ret.reverse()
		return ret



'''
root = Node([1,2])
child1 = Node([0,5])
root.add_child(child1)
child2 = Node([0,1,4])
root.add_child(child2)
grandchild1 = Node([99])
child1.add_child(grandchild1)
root.print_tree()
'''


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


def bfs(s0,s1):
	frontier = []
	explored = []
	root = Node(s0)
	to_add, tree = get_succ(root)
	for i in to_add: frontier.append(i)
	x = 0
	while(x < 10000): #some max bound just in case
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
	

def dfs(s0,s1):
	frontier = []
	explored = []
	root = Node(s0)
	to_add, tree = get_succ(root)
	for i in to_add: frontier.append(i)
	x = 0
	while(x < 10000): #some max bound just in case
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



# okay, this is not doing iddfs correctly... so this is basically just a placerholder method
# I'll get it straightened out if I have time
def iddfs(s0,s1):
	
	y = 1
	while y < 100: #some max bound just in case
		print y
		y+=1

		frontier = []
		explored = []
		root = Node(s0)
		to_add, tree = get_succ(root)
		for i in to_add: frontier.append(i)

		x = 0
		while(x < y): #this is the deepening loop
			x+=1

			if (len(frontier) <= 0): return False, "fail0"

			leaf = frontier.pop() 

			if is_solution(leaf.data, s1): 
				return True, (root, leaf, y)
				#root.print_solution(leaf)

			explored.append(leaf)

			to_add, tree = get_succ(leaf)

			for i in to_add:
				if i not in frontier:
					if i not in explored:
						frontier.append(i)

	return False, "fail1 - exceeded max depth of: "+str(y)


def astar(s0,s1):
	print "nice!"



def format_output(arr):
	ret = "length of solution path: "+ str(len(arr)) + "\n\n"
	ret += "solution: \n"
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
	if (len(argv) == 0): return 0 

	init_state = parse_input(argv[0])
	goal_state = parse_input(argv[1])
	print "init state"
	print_state(init_state)
	print "goal state"
	print_state(goal_state)

	solution = []

	which = argv[2]
	print "running: ",which,"\n"
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

		to_out = ""

		if solution[0]:
			r = solution[1][0]
			l = solution[1][1]
			as_an_array = r.print_solution(l)
			to_out = format_output(as_an_array)
			to_out = "expanded nodes: " + str(solution[1][2]-1) + "\n\n" + to_out
			print to_out
			
		else:
			print solution[1]
			to_out = solution[1]

		output = open(argv[3], 'w+') 
		output.write(to_out)
		output.close()


if __name__ == "__main__":
   main(sys.argv[1:])



