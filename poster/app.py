from flask import Flask, request
from keras.models import load_model
import numpy as np

encoder = load_model(r'./codes/weights/encoder_weights.h5')

app = Flask(__name__)

def preprocessQuestion(user_query):
    # TODO(zwen)
	return user_query

def generateInitialVector(cleanedQuery):
    # TODO(zwen)
    return [0, 0, 0]

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

@app.route('/', methods=['POST'])
def query():
    user_query = request.form['query']
    print("user_query: ", user_query)

    # calculate the vector for user_query
    cleanedQuery = preprocessQuestion(user_query)
    initial_vector = generateInitialVector(cleanedQuery)
    print("initial_vector: ", initial_vector)

    return "received"



if __name__ == '__main__':
    app.run()
