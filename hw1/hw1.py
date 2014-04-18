import sys

'''
this.py
< initial puzzle state file >
< goal puzzle state file >
< mode >
< output file >

bfs
dfs 
iddfs
astar 

'''


class Node(object):
	def __init__(self, data, parent=None):
		self.data = data
		self.children = []
		self.parent = parent

	def add_child(self, obj):
		self.children.append(obj)
		#the last child is the one just added
		self.children[-1].parent = self 


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

def get_successors(state):
	ret = []
	swaps = get_possible_swaps(state)
	for i in xrange(len(swaps)):
		if swaps[i] == 1:
			new_state = do_swap(state,i)

			new_node = (new_state, state)

			ret.append(new_node)
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


def bfs(s0,s1):
	frontier = []
	to_add = get_successors(s0)
	for i in to_add:
		frontier.append(i)
	explored = []

	x = 0
	while(x < 20000): #some max bound just in case
		x+=1

		if (len(frontier) <= 0): return "fail"

		leaf = frontier.pop(0) 

		if is_solution(leaf[0],s1):
			print x, "iterations"
			return ("found it", leaf, explored)

		explored.append(leaf)

		to_add = get_successors(leaf[0])

		for i in to_add:
			if i not in frontier:
				if i not in explored:

					frontier.append(i)


def dfs(s0,s1):
	frontier = get_successors(s0)
	explored = []
	x = 0
	while(x < 10000): #some max bound just in case
		x+=1
		if (len(frontier) <= 0): return "fail"
		leaf = frontier.pop() 
		if is_solution(leaf,s1):
			print x, "iterations"
			return ("found it", leaf)
		explored.append(leaf)
		to_add = get_successors(leaf)
		for i in to_add:
			if i not in frontier:
				if i not in explored:
					frontier.append(i)
	return ("oops! reached max of:", x)


def trace_solution(s,start_state):

	solution = []

	all_explored = s[2]

	state = s[1]
	solution.append(state[0])
	solution.append(state[1])

	x = 0
	while x < 100:
		x += 1
		for i in all_explored:
			if i[0] == start_state and i[0] == state[1]:	
				solution.reverse()
				return solution

			if i[0] == state[1] and i[1] not in solution:
				state = i
				solution.append(state[1])

	solution.reverse()
	return solution


def main(argv):

	init_state = parse_input(argv[0])
	goal_state = parse_input(argv[1])
	print "init state"
	print_state(init_state)
	print "goal state"
	print_state(goal_state)

	solution = []

	which = argv[2]
	print "running: ",which
	if (which == 'bfs'):
		solution = bfs(init_state,goal_state)
	elif (which == 'dfs'):
		solution = dfs(init_state,goal_state)
	elif (which == 'iddfs'):
		print "iddfs"
	elif (which == 'astar'):
		print "astar"
	else:
		print "unknown command:", which
		print "exiting..."
		sys.exit()

	if len(solution) > 0:
		print "solution:"
		show_sol = trace_solution(solution,init_state)
		print len(show_sol)
		for i in show_sol: print_state(i)

	output = open(argv[3], 'w+') 
	output.write(str(solution[1]))
	output.close()



if __name__ == "__main__":
   main(sys.argv[1:])



