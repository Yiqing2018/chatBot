
DATA_DIR = '../quora-question-pairs/'
train_path = DATA_DIR + 'train.csv'
test_path = DATA_DIR + 'test.csv'
sample_train_path = DATA_DIR + 'sample_train.csv'
sample_test_path = DATA_DIR + 'sample_test.csv'

f = open(train_path, 'r')
lines = f.readlines()
f.close()

f = open(sample_train_path, 'w')
for i in range(100):
	line = lines[i]
	f.write(line)
f.close()

f = open(test_path, 'r')
lines = f.readlines()
f.close()

f = open(sample_test_path, 'w')
for i in range(10):
	line = lines[i]
	f.write(line)
f.close()