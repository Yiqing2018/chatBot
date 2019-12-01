from keras.models import load_model
import numpy as np

encoder = load_model(r'./weights/encoder_weights.h5')
decoder = load_model(r'./weights/decoder_weights.h5')

def test(data):
	inputs = np.array([data[0]])
	x = encoder.predict(inputs)
	y = decoder.predict(x)
	print('Input: {}'.format(inputs))
	print('Encoded: {}'.format(x))
	print('Decoded: {}'.format(y))	
