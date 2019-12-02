from keras.models import load_model
import numpy as np
import autoencoder
import math

encoder = load_model(r'./weights/encoder_weights.h5')
decoder = load_model(r'./weights/decoder_weights.h5')
encoder_decoder = load_model(r'./weights/ae_weights.h5')

def eval(data):
	diff = list()
	for i in range(len(data)):
		x = np.array([data[i]])
		y = encoder.predict(x)
		z = decoder.predict(y)
		
		# print('Input: {}'.format(x))
		# print('Encoded: {}'.format(y))
		# print('Decoded: {}'.format(z))

		diff.append(vectorSimilarity(x[0], z[0]))
	print("evaluation on test data, similarity = ", sum(diff) / len(diff) )


# according to our theory, the similarity of two vectors is measured by 
# cosφ, more close to 1, more silimar
def vectorSimilarity(a,b):
	res = 0
	aSize = 0
	bSize = 0
	for i in range(len(a)):
		n1 = int(a[i])
		n2 = int(b[i])
		res += (n1 * n2)
		aSize += (n1 * n1)
		bSize += (n2 * n2)
	return res/math.sqrt(aSize * bSize)

def main():
    # load full data
    data = autoencoder.loadQuestionsFromDB(-1)    
    # load vocabulary
    vocabulary = autoencoder.load_vocabulary()
    print("Vocabulary loaded and get the dictionary")
    # clean up data
    cleanedData, _ = autoencoder.preprocess(data, vocabulary)
    print("Data preprocessed")
    # extract test data
    idx = int(len(cleanedData)*autoencoder.trainingPercent)
    testData = cleanedData[idx:]
    print("Split testData")
    # evaluate the result
    eval(testData)

if __name__ == '__main__':
	main()
