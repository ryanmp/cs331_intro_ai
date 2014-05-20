
def parse_input(file_name):
	f = open(file_name)
	ret = [x.strip() for x in f.readlines()]
	return ret


def get_vocab(train_data, stop_list):
	flattened = [item for sublist in train_data for item in sublist]
	ret = list(set(flattened) - set(stop_list))
	ret.sort
	return ret


def featurize_data(vocab, data):
	featurized_data = []
	for line in data:
		features = []
		for i in vocab:
			if i in line:
				features.append(1)
			else:
				features.append(0)
		features.append(0) # one extra 0 for...
		featurized_data.append(features)
	return featurized_data


def out_to_preprocessed(vocab,f_data,out_file_name):
	f = open(out_file_name, "wb")
	for i in vocab:
		f.write(str(i)+",")
	f.write("\n")

	for line in f_data:
		for i in line:
			f.write(str(i)+",")
		f.write("\n")

	f.close()


x = [ i.split(' ') for i in parse_input('traindata.txt')]
y = parse_input('stoplist.txt')

vocab = get_vocab(x,y)


f_data = featurize_data(vocab, x)

out_to_preprocessed(vocab,f_data,'preprocessed.txt')





