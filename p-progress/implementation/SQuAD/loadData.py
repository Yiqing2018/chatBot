import json

with open('train-v2.0.json', 'r') as f:
    line = f.readline()
    data_json = json.loads(line)['data']
    print(type(data_json))
    for i in range(10):
    	d = data_json[i]
    	paragraphs = d['paragraphs']
    	for i in range(len(paragraphs)):
    		print('similar questions')
    		par = paragraphs[i]
    		qas = par['qas']
    		for i in range(len(qas)):
    			qa = qas[i]
    			question = qa['question']
    			question_id = qa['id']
    			print(question)
    f.close()
