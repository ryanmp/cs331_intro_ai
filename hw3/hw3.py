import math

def parse_data(file_name):
	f = open(file_name)
	ret = [x.strip() for x in f.readlines()] #grab lines, remove newline character
	ret = [ i.split(' ') for i in ret] #separate words
	return ret

def parse_list(file_name):
	f = open(file_name)
	ret = [x.strip() for x in f.readlines()]
	return ret

def get_vocab(train_data, stop_list):
	flattened = [item for sublist in train_data for item in sublist]
	#ret = list(set(flattened) - set(stop_list)) # remove words on stop list from vocab
	ret = list(set(flattened))
	ret.sort
	return ret

def featurize_data(vocab, data, labels):
	featurized_data = []
	for line, label in zip(data, labels):
		features = []
		for i in vocab:
			if i in line: features.append(1)
			else: features.append(0)
		features.append(int(label))
		featurized_data.append(features)
	return featurized_data

def out_to_preprocessed(vocab,f_data,out_file_name):
	f = open(out_file_name, "wb")
	for i in vocab: # first line contains vocab
		f.write(str(i)+",")
	f.write("\n")
	for line in f_data: # now the rest of the lines are f_data vectors
		for i in line:
			f.write(str(i)+",")
		f.write("\n")
	f.close()

def calc_bd(labels):
	t = [int(i) for i in labels]
	return sum(t)/float(len(labels)) # this is the value for T

def calc_probs(f_data):
	ret = []
	for line in f_data:
		temp_line = []
		for i in line:
			temp = i + 1
			temp = float(temp)/len(line)
			temp_line.append(temp)
		ret.append(temp_line)
	return ret



traindata = parse_data('traindata.txt')
testdata = parse_data('testdata.txt')

trainlabels = parse_list('trainlabels.txt')
testlabels = parse_list('testlabels.txt')

stoplist = parse_list('stoplist.txt')

vocab = get_vocab(traindata,stoplist)

f_traindata = featurize_data(vocab, traindata, trainlabels)
f_testdata = featurize_data(vocab, testdata, testlabels)
out_to_preprocessed(vocab,f_traindata,'preprocessed.txt') # 50 points

# calculate bd probability (# with T over total)
p_bd = calc_bd(trainlabels)

#f_probs = calc_probs(f_traindata)






class_0_ints = [0 for i in xrange(len(vocab))] #fortune
class_1_ints = [0 for i in xrange(len(vocab))] #future
for i in xrange(len(traindata)): # for each saying
	for j in traindata[i]: # for each word in saying
		if j in vocab:
			idx = vocab.index(j)
			if trainlabels[i] == '0':
				class_0_ints[idx] += 1

			if trainlabels[i] == '1':
				class_1_ints[idx] += 1


t = [int(i) for i in trainlabels]
true_sum = sum(t)
false_sum = len(trainlabels) - true_sum

class_0_probs = []
for i in class_0_ints:
	total = sum(class_0_ints)
	temp = math.log(float(i+1)/(total+false_sum))
	class_0_probs.append(temp)

class_1_probs = []
for i in class_1_ints:
	total = sum(class_1_ints)
	temp = math.log(float(i+1)/(total+true_sum))
	class_1_probs.append(temp)


def test_one(which, data):
	t_data_one = [i for i in data[which]]

	# run 'it'
	sum0 = math.log(1 - p_bd)
	sum1 = math.log(p_bd)
	new0, new1 = 0, 0
	for i in xrange(len(t_data_one)-1):
		new0 = t_data_one[i] * class_0_probs[i]
		new1 = t_data_one[i] * class_1_probs[i]
		sum0 += new0
		sum1 += new1

	if sum0 > sum1:
		return 0
	else:
		return 1

def test_all(data):
	results = []
	for i in xrange(len(data)):
		temp = test_one(i,data)
		results.append(temp)
	return results

def check_results(results, labels):
	number_correct = 0
	for i in xrange(len(labels)):
		if labels[i] == str(results[i]):
			number_correct += 1
	return float(number_correct)/len(labels)






results = test_all(f_traindata)
print check_results(results,trainlabels)

results = test_all(f_testdata)
print check_results(results,testlabels)



'''
def main(args):
	print args

if __name__ == '__main__':
	import sys
	main(sys.argv[1:])
	'''


