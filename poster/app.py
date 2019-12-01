from flask import Flask, request
from keras.models import load_model
import numpy as np
from dataprocessor import cleanQuestion
from autoencoder import load_vocabulary, generate_initial_vector
import keras

encoder = load_model(r'./weights/encoder_weights.h5')
vocabulary = load_vocabulary()
app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['POST'])
def query():
    user_query = request.form['query']
    print("user_query: ", user_query)

    # calculate the vector for user_query
    question_words = cleanQuestion(user_query)
    print("question_words: ", question_words)
    initial_vector = generate_initial_vector(question_words, vocabulary)
    print("initial_vector: ", initial_vector)
    encode = keras.preprocessing.sequence.pad_sequences(
        [initial_vector], 
        value=0, # 0 is for pad
        padding="post",
        maxlen=36)
    compressed_vector = encoder.predict(encode)[0]
    print("compressed_vector: ", compressed_vector)

    # TODO(zwen): go over saved trained vectors and calculate distance
    return "received"


if __name__ == '__main__':
    app.run()
