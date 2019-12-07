import os, pprint
import numpy as np
import tensorflow as tf
import keras
from keras.layers import Input, Dense
from keras.models import Model
from keras.callbacks import TensorBoard
from google.cloud import bigquery
from preprocessor import preprocess

trainingPercent = 0.8
maxlen = 36
epochs_size = 3
compressed_size = 10

class AutoEncoder:
    def __init__(self,trainingData):
        self.trainingData = trainingData

    def encoder(self):
        inputs = Input(shape=(self.trainingData[0].shape))
        hidden_1 = Dense(20, activation='sigmoid')(inputs)
        outputs = Dense(compressed_size, activation='relu')(hidden_1)
        model = Model(inputs, outputs)

        self.encoder = model
        return model

    def decoder(self):
        inputs = Input(shape=(compressed_size,))
        hidden_1 = Dense(20, activation='relu')(inputs)
        outputs = Dense(maxlen, activation='sigmoid')(hidden_1)
        model = Model(inputs,outputs)
        self.decoder = model
        return model

    def encoder_decoder(self):
        ec = self.encoder()
        dc = self.decoder()
        inputs = Input(shape=self.trainingData[0].shape)
        ec_out = ec(inputs)
        dc_out = dc(ec_out)
        model = Model(inputs, dc_out)
        self.model = model
        return model

    def fit(self, batch_size, epochs):
        self.model.compile(optimizer='sgd', loss='mse')
        log_dir = './log/'
        tbCallBack = keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=0, write_graph=True, write_images=True)
        self.model.fit(self.trainingData, self.trainingData,
                        epochs=epochs,
                        batch_size=batch_size,
                        callbacks=[tbCallBack])
    def save(self):
        if not os.path.exists(r'./weights'):
            os.mkdir(r'./weights')
        self.encoder.save(r'./weights/encoder_weights.h5')
        self.decoder.save(r'./weights/decoder_weights.h5')
        self.model.save(r'./weights/ae_weights.h5')
            

    def run(self):
        self.encoder_decoder()
        self.fit(batch_size=50, epochs=epochs_size)
        self.save()

