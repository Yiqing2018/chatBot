from keras.models import load_model
import numpy as np
import run, fetchData
import math

encoder = load_model(r'./weights/encoder_weights.h5')
decoder = load_model(r'./weights/decoder_weights.h5')
encoder_decoder = load_model(r'./weights/ae_weights.h5')

def eval(data):
	diff = list()
	for i in range(len(data)):
	# for i in range(1):
		x = np.array([data[i]])
		y = encoder.predict(x)
		z = decoder.predict(y)
		
		print('Input: {}'.format(x))
		print('Encoded: {}'.format(y))
		print('Decoded: {}'.format(z))

		diff.append(vectorSimilarity(x[0], z[0]))
	print("evaluation on test data, similarity = ", sum(diff) / len(diff) )


# according to our theory, the similarity of two vectors is measured by the cosφ
def vectorSimilarity(a,b):
	res = 0
	aSize = 0
	bSize = 0
	for i in range(len(a)):
		res += (a[i] * b[i])
		aSize += (a[i] * a[i])
		bSize += (b[i] * b[i])
	return res/(aSize * bSize)

def main():
	# fetch data
	data = fetchData.getData()
	# extract test data - original
	idx = int(len(data)*run.trainingPercent)
	testData = data[idx:]
	# convert string into long vector
	cleanData = run.AutoEncoder(testData).preprocess()
	# evaluate the result
	eval(cleanData)

if __name__ == '__main__':
	main()
