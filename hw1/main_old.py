'''

todo:

restructured as to more easily accomodate more algos,

right now it's just depth first...

but we will need depth, breadth, and more...


hueristics for a*:

+how many tiles are in the correct spot
+how many moves away is each tile from the correct spot (better?)

'''

import sys, time
from sets import Set
sys.setrecursionlimit(10000)

class Node(object):
	def __init__(self, data, parent=None):
		self.data = data
		self.children = []
		self.parent = parent

	def add_child(self, obj):
		self.children.append(obj)
		#the last child is the one just added
		self.children[-1].parent = self 

def print_tree(t):
	x = 0
	def inner(t,x):
		x+=1
		if (t != None):
			print x, t.data, t.parent
			if (len(t.children) > 0):
				for i in t.children:
					if (i != None):
						y = x 
						inner(i,y)
	inner(t,x)



'''
#for testing our tree

t = Node("this")

c1 = Node("is")
c2 = Node("a")
t.add_child(c1)
t.add_child(c2)

gc1 = Node("grandchild")
c1.add_child(gc1)

print_tree(t)
'''

def leaf_to_root(n):
	ret = []
	def inner(n):
		ret.append(n)
		if (n.parent):
			inner(n.parent)
	inner(n)
	for i in ret:
		print i.parent, i
		print_state(i.data)


def solution_length(n):
	ret = []
	def inner(n):
		ret.append(n)
		if (n.parent):
			inner(n.parent)
	inner(n)
	return len(ret)


visited_states = Set()


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


def get_idx(state,num):
	ret = (0,0)
	for i in xrange(len(state)):
		for j in xrange(len(state[i])):
			if state[i][j] == 0:
				ret = (i,j)
	return ret


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


def get_successors(state):
	ret = []
	swaps = get_possible_swaps(state)
	for i in xrange(len(swaps)):
		if swaps[i] == 1:
			new_state = do_swap(state,i)
			if serialize(new_state) not in visited_states:
				ret.append(new_state)
	return ret


def is_solution(current_state, goal_state):
	ret = True;
	for i in xrange(3):
		for j in xrange(3):
			if current_state[i][j] != goal_state[i][j]:
				ret = False
	return ret


def print_solution(sol):
	for i in sol:
		print_state(i)


def recursion(current_state, goal_state,x,sol):
	print_tree(sol)
	new_node = Node(current_state)
	sol.add_child(new_node)
	visited_states.add(serialize(current_state))
	#a way to show progress
	#print len(visited_states)
	if is_solution(current_state,goal_state):
		return new_node, sol
	else:
		# the check for in visited_states is done here
		next_states = get_successors(current_state) 
		for i in next_states:
			if x < 3: # some limit just in case
				x += 1
				#ret, sol = recursion(i, goal_state,x,sol)
				out = recursion(i, goal_state,x,sol)
				if out:
					out[0] = ret
				#if ret: return ret, sol
	

def recursive_solver(s0, s1):
	solution = []
	tree = Node(s0)
	final_node = Node('')
	next_states = get_successors(s0)
	for i in next_states:
		child1 = Node(i)
		tree.add_child(child1)
		if is_solution(i,s1):
			final_node = child1
			return final_node
		next_states2 = get_successors(i)
		for j in next_states2:
			child2 = Node(j)
			child1.add_child(child2)
			if is_solution(j,s1):
				final_node = child2
				return final_node
	return "no solution"


def recursive_solver2(s0, s1):
	solution = []
	tree = Node(s0)
	final_node = Node('')
	def inner(s0,s1,tree,final_node):
		visited_states.add(serialize(s0))
		next_states = get_successors(s0)
		for i in next_states:
			child1 = Node(i)
			tree.add_child(child1)
			if is_solution(i,s1):
				return child1
			ret = inner(i,s1,child1,final_node)
			if (ret): return ret
	return inner(s0,s1,tree,final_node)


def solver2(s0,s1):
	visited = Set()
	fringe = []
	visited.add(serialize(s0))
	fringe.append(serialize(s0))
	out = get_successors(s0)
	while len(fringe) != 0:
		for i in xrange(len(fringe)):
			idx = unserialize(fringe[i])
			is_solution(idx,s1)
			next_states = get_successors(idx)
			for j in next_states:
				visited.add(serialize(j))
				fringe.append(serialize(j))
				print fringe




def solver(s0,s1):

	frontier = get_successors(s0)
	explored = []

	x = 0
	while(x < 20000): #some max bound just in case
		x+=1

		if (len(frontier) <= 0): return "fail"

		# pop(0) does fifo, which implements bfs
		# pop() does lifo, which implements dfs


		leaf = frontier.pop(0) 


		if is_solution(leaf,s1):
			print x
			return ("found it", leaf)
		explored.append(leaf)

		to_add = get_successors(leaf)
		for i in to_add:
			if i not in frontier:
				if i not in explored:
					frontier.append(i)



def unserialize(x):
	ret = [[i for i in xrange(3)] for i in xrange(3)]
	for i in xrange(9):
		ret[i/3][i%3] = int(x[i])
	return ret

def serialize(state):
	ret = ''
	for i in xrange(3):
		for j in xrange(3):
			ret += str(state[i][j])
	return ret

def main():
	init_state = parse_input('testStart4.txt')
	goal_state = parse_input('testGoal1.txt')


	print "init state"
	print_state(init_state)
	print "goal state"
	print_state(goal_state)

	start_time = time.time()
	print solver(init_state,goal_state)
	print time.time()-start_time

	'''
	out = recursive_solver2(init_state,goal_state)
	print solution_length(out)
	'''

	'''
	solution_tree = Node('root')
	start_time = time.time()
	x, solution_tree = recursion(init_state, goal_state,0,solution_tree)
	print x
	print solution_tree
	print time.time()-start_time
	
	print "init state"
	print_state(init_state)
	print "goal state"
	print_state(goal_state)

	leaf_to_root(x)


	#print_tree(solution_tree)

	#print(len(solution))

	#uh oh... this prints every attempted node... not just the current path
	#print_solution(solution)
	#print_state(solution[-1])
	'''

main()


