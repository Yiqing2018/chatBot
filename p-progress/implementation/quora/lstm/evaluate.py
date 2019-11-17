import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np


DATA_DIR = '../quora-question-pairs/'
TEST_DATA_FILE = DATA_DIR + 'sample_test.csv'

actual = list()
with open(TEST_DATA_FILE) as f:
	reader = csv.DictReader(f)
	for row in reader:
		actual.append(row['is_duplicate'])
f.close()

f = open('output.txt', 'r')
lines = f.readlines()
f.close()

predict_list = []
actual_list = []

zero_one_count = 0
one_zero_count = 0
count = 0
for i in range(len(lines)):
	line = lines[i]
	predict_val = int(line)
	actual_val = int(actual[i])

	actual_list.append(actual_val)
	predict_list.append(predict_val)
	# print("predict", int(line), "actual", int(actual[i]))
	if actual_val == predict_val :
		count += 1
	if actual_val == 0 and predict_val == 1:
		zero_one_count += 1
	if actual_val == 1 and predict_val == 0:
		one_zero_count += 1

print(count/len(lines))

# x1 = range(99)
# y1 = actual_list 
# x2 = range(99)
# y2 = predict_list
# plt.figure(figsize=(20,4))
# l1=plt.plot(x1,y1,'b--',label='actual')
# l2=plt.plot(x2,y2,'g--',label='prediction')

# plt.title('evaluation of LSTM model')
# plt.xlabel('data')
# plt.ylabel('is_duplicate')
# plt.legend()
# plt.show()

label_list = ["correct", "error-negative", "error-positive"]  
size = [count, zero_one_count, one_zero_count]   
color = ["gray", "peru", "moccasin"]
explode = [0.05, 0, 0] 
patches, l_text, p_text = plt.pie(size, explode=explode, colors=color, labels=label_list, labeldistance=1.1, autopct="%1.1f%%", shadow=False, startangle=90, pctdistance=0.6)
plt.axis("equal") 
plt.title('evaluation of LSTM model')
plt.legend()
plt.show()

