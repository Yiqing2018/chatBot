
import csv
from collections import defaultdict

with open('sample_test.csv', mode='w') as csv_file:
    fieldnames = ['test_id', 'question1', 'question2', 'is_duplicate']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    with open('train.csv') as f:
    	reader = csv.DictReader(f)
    	rows=[r for r in reader]
    	test_id = 0
    	for i in range(1001,1100):
    		row = rows[i]
    		qa1 = row['question1']
    		qa2 = row['question2']
    		score = row['is_duplicate']
    		writer.writerow({'test_id': test_id, 
				'question1': qa1, 
				'question2': qa2,
				'is_duplicate': score})
    		test_id += 1

    f.close()
csv_file.close()

f = open("train.csv", 'r')
lines = f.readlines()
f.close()

f = open("sample_train.csv", 'w')
for i in range(1000):
	line = lines[i]
	f.write(line)
f.close()