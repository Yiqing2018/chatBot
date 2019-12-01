import os, pprint
import numpy as np
import tensorflow as tf
import keras
from dataprocessor import cleanQuestion
from keras.layers import Input, Dense
from keras.models import Model
from keras.callbacks import TensorBoard
from google.cloud import bigquery

trainingPercent = 0.8
maxlen = 36
epochs_size = 3
compressed_size = 10
data_size = 1000000 # set limitedDataSet to True
limitedDataSet = False
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

def queryTable(client, dataset_id, sql):
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(
        sql,
        location='US',
        job_config=job_config)
    return query_job.result()  # Waits for the query to finish

def loadQuestionsFromDB():
    client = bigquery.Client()
    dataset_id = "stackoverflow" # dataset_id used for query shouldn't contain project_id.
    if limitedDataSet:
        query = """
        SELECT
            *
        FROM
            `optical-metric-260620.stackoverflow.questions`
        LIMIT {};
        """.format(data_size)
    else:
        query = """
        SELECT
            *
        FROM
            `optical-metric-260620.stackoverflow.questions`;
        """
    result = queryTable(client,dataset_id, query)
    return result

def preprocess(data, vocabulary):
    trainingData = []
    for row in data:
        sample = []
        words = cleanQuestion(row[1])
        for word in words:
            if word in vocabulary:
                sample.append(vocabulary[word])
            else:
                sample.append(1) # 1 is for unknown
        trainingData.append(sample)
    # make sure the length of input is the same
    return keras.preprocessing.sequence.pad_sequences(
        trainingData, 
        value=0, # 0 is for pad
        padding="post",
        maxlen=36)

def generate_initial_vector(words, vocabulary):
    sample = []
    for word in words:
        if word in vocabulary:
            sample.append(vocabulary[word])
        else:
            sample.append(1) # 1 is for unknown
    return sample

def load_vocabulary():
    client = bigquery.Client()
    dataset_id = "stackoverflow"
    query = """
        SELECT 
            *
        FROM 
            `optical-metric-260620.stackoverflow.vocabulary`;
    """
    result = queryTable(client, dataset_id, query)
    vocabulary = {}
    for row in result:
        vocabulary[row[0]] = row[1]
    return vocabulary

def main():
    data = loadQuestionsFromDB()
    print("Data loaded from DB.questions")

    vocabulary = load_vocabulary()
    print("Vocabulary loaded and get the dictionary")

    cleanedData = preprocess(data, vocabulary)
    print("Data preprocessed")

    # split training data and test data
    idx = int(len(cleanedData)*trainingPercent)
    trainingData = cleanedData[:idx]
    testData = cleanedData[idx:]

    # train model
    autoEncoder = AutoEncoder(trainingData)
    autoEncoder.run()
    

if __name__ == '__main__':
    main()