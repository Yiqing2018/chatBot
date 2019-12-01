# apply the encoder model on dataset
from keras.models import load_model
from google.cloud import bigquery
import os
import string
import numpy as np
import fetchData, run

encoder = load_model(r'./weights/encoder_weights.h5')

def updateResult(result):
	client = bigquery.Client()
	dataset_id = "stackoverflow" # dataset_id used for query shouldn't contain project_id.

def main():
	data = fetchData.getData()
	cleanData = run.AutoEncoder(data).preprocess()
	result = list()
	for i in range(len(cleanData)):
		x = np.array([cleanData[i]])
		y = encoder.predict(x)
		result.append([cleanData[i][0], np.array_str(y[0])]) # qid, short vector
		print(result[i])

	updateResult(result)

	# add attribute on console
	# insert attribute




if __name__ == '__main__':
	main()


