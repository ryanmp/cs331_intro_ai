'''
todo:

dirichletic priors?

add one to numerator...
add two to denominator... #2 classes



first term...

p(bd)...
first we need to determine just the likelihood that fortune = true/false
(should be roughly .5 ??)



second term...

# of times (w = false AND c = false)     + 1
------
# of times c = false                    + 2




then multiple first part by set of 'second terms'




....


what should we expect for accuracy?

results1: accuracy should be in the 90s%
running the test on the training data

results2: accuracy should be in the 70s-80s%
running the test on the testing data


'''



import math


def parse_input(file_name):
	f = open(file_name)
	ret = [x.strip() for x in f.readlines()]
	return ret



def get_vocab(train_data, stop_list):
	flattened = [item for sublist in train_data for item in sublist]
	#ret = list(set(flattened) - set(stop_list)) # remove words on stop list from vocab
	ret = list(set(flattened))
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


def out_to_results(results,file_name):
	f = open(file_name, "wb")
	for i in results:
		f.write(str(i) + "\n")
	f.close()






# add one
def test_one(x):
	t_data_one = [i for i in t_data[x]]

	# run 'it'
	sum0 = 0
	sum1 = 0
	new0 = 0
	new1 = 0
	for i in xrange(len(t_data_one)-1):
		new0 = t_data_one[i] * class_0[i]
		new1 = t_data_one[i] * class_1[i]
		sum0 += new0
		sum1 += new1

	if sum0 > sum1:
		return 0
	else:
		return 1



x = [ i.split(' ') for i in parse_input('traindata.txt')]
y = parse_input('stoplist.txt')
z = parse_input('trainlabels.txt')




vocab = get_vocab(x,y)


f_data = featurize_data(vocab, x)

out_to_preprocessed(vocab,f_data,'preprocessed.txt')


# add one smoothing
class_0_ints = [0 for i in xrange(len(vocab))] #fortune
class_1_ints = [0 for i in xrange(len(vocab))] #future

# for each saying
for i in xrange(len(x)):

	# for each word in saying
	for j in x[i]:

		# if this word is in our vocab
		if j in vocab:

			idx = vocab.index(j)

			#which class does this saying belong to?
			if z[i] == '0':
				class_0_ints[idx] += 1

			if z[i] == '1':
				class_1_ints[idx] += 1




# dividing sums by totals
# adding direcht priors

class_0 = [1 for i in class_0_ints]
class_1 = [1 for i in class_1_ints]

total = float(sum(class_0_ints)+sum(class_1_ints))

for i in xrange(len(class_0)):
	class_0[i] = (class_0_ints[i]+1)/(total+2)

for i in xrange(len(class_1)):
	class_1[i] = (class_1_ints[i]+1)/(total+2)





# oh we should run it on the training data too....

t1 = [ i.split(' ') for i in parse_input('traindata.txt')]
t_data = featurize_data(vocab, t1)

# test all
results = []
for i in xrange(len(t_data)):
	temp = test_one(i)
	results.append(temp)

# compare results to testlabels
true_test_labels = parse_input('trainlabels.txt')

number_correct = 0
for i in xrange(len(true_test_labels)):
	if true_test_labels[i] == str(results[i]):
		number_correct += 1
print float(number_correct)/len(true_test_labels)







# running it on the testing data

t1 = [ i.split(' ') for i in parse_input('testdata.txt')]
t_data = featurize_data(vocab, t1)

# test all
results = []
for i in xrange(len(t_data)):
	temp = test_one(i)
	results.append(temp)

# compare results to testlabels
true_test_labels = parse_input('testlabels.txt')

number_correct = 0
for i in xrange(len(true_test_labels)):
	if true_test_labels[i] == str(results[i]):
		number_correct += 1
print float(number_correct)/len(true_test_labels)



















