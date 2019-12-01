import os, pprint
import fetchData, test
import numpy as np
import tensorflow as tf
import keras
from keras.layers import Input, Dense
from keras.models import Model
from keras.callbacks import TensorBoard


trainingPercent = 0.8
long_dimension = 20
short_dimension = 5

class AutoEncoder:
	def __init__(self,trainingData):
		self.trainingData = trainingData

	def preprocess(self):
		# build vocabulary dict
		trainingData = self.trainingData
		tokens = []
		for row in trainingData:
			text = row[1]
			tokenized = text.split(' ') #Let's tokenize our text by just take each word
			tokens = tokens + tokenized
		vocab = {k:(v+2) for v,k in enumerate(np.unique(tokens))}
		vocab['<PAD>'] = 0
		vocab['<UNK>'] = 1
		# pprint.pprint(vocab)
		# convert the string input to a numerical vector
		train = []
		for row in trainingData:
			sample = []
			for word in row[1].split(" "):
				if word in vocab:
					sample.append(vocab[word])
				else:
					sample.append(vocab['<UNK>'])
			train.append(sample)
		# make sure the length of input is the same
		self.train = keras.preprocessing.sequence.pad_sequences(
			train, 
			value=vocab['<PAD>'],
			padding = "post",
			maxlen = long_dimension)
		return self.train

	def encoder(self):
		inputs = Input(shape=(self.train[0].shape))
		# add more layers!
		encoded = Dense(short_dimension, activation='relu')(inputs)
		model = Model(inputs, encoded)
		self.encoder = model
		return model

	def decoder(self):
		inputs = Input(shape=(short_dimension,))
		decoded = Dense(long_dimension)(inputs)
		model = Model(inputs, decoded)
		self.decoder = model
		return model

	def encoder_decoder(self):
		ec = self.encoder()
		dc = self.decoder()
		inputs = Input(shape=self.train[0].shape) # long vector
		ec_out = ec(inputs) # short vector
		dc_out = dc(ec_out) # long vector trained by model
		model = Model(inputs, dc_out)
		self.model = model
		return model

	def fit(self, batch_size, epochs):
		self.model.compile(optimizer='sgd', loss='mse')
		log_dir = './log/'
		tbCallBack = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0, write_graph=True, write_images=True)
		self.model.fit(self.train, self.train,
                        epochs=epochs,
                        batch_size=batch_size,
                        callbacks=[tbCallBack])
	def save(self):
		if not os.path.exists(r'./weights'):
			os.mkdir(r'./weights')
		else:
			self.encoder.save(r'./weights/encoder_weights.h5')
			self.decoder.save(r'./weights/decoder_weights.h5')
			self.model.save(r'./weights/ae_weights.h5')
	def run(self):
		self.preprocess()
		self.encoder_decoder()
		self.fit(batch_size=50, epochs=300)
		self.save()

	


def main():
	# fetch data
	data = fetchData.getData()
	# print(data)
	# split training data and test data
	idx = int(len(data)*trainingPercent)
	trainingData = data[:idx]
	TestData = data[idx:]
	# train our model
	autoEncoder = AutoEncoder(trainingData)
	autoEncoder.run()


if __name__ == '__main__':
	main()