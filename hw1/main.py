def parse_input(file_name):
	f = open(file_name)
	lines_raw = f.readlines()
	ret = []
	ret_dict = {}
	for i in range(0,len(lines_raw)):
		parsing_line = []
		parsing_line = lines_raw[i].split(',')
		parsing_line = map(int, parsing_line)
		#to_tuple = (parsing_line[1],parsing_line[2])
		ret.append(parsing_line)

	for i in xrange(3):
		for j in xrange(3):
			ret_dict[(i,j)] = ret[i][j]
	return ret_dict

def main():
	init_state = parse_input('testStart1.txt')
	print init_state
	#print init_state[0].index(0)


main()