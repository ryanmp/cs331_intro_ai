import sys

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
			ret.append(do_swap(state,i))
	return ret

def main():
	init_state = parse_input('testStart1.txt')
	print "starting state:"
	print_state(init_state)

	new_states = get_successors(init_state)

	print "next states:"
	for i in new_states:
		print_state(i)


	next_state = new_states[0]

	print "new state:"
	print_state(next_state)

	new_states = get_successors(next_state)

	print "next states:"
	for i in new_states:
		print_state(i)




	







main()