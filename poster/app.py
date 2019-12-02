from flask import Flask, request
from keras.models import load_model
import numpy as np
from dataprocessor import cleanQuestion, queryTable
from autoencoder import load_vocabulary, generate_initial_vector
import keras
from google.cloud import bigquery
from evaluate import vectorSimilarity

encoder = load_model(r'./weights/encoder_weights.h5')
vocabulary = load_vocabulary()
client = bigquery.Client()
dataset_id = "stackoverflow"

app = Flask(__name__)

def load_question_vector():
    query = """
        SELECT 
            *
        FROM 
            `optical-metric-260620.stackoverflow.compressed_vectors`;
    """
    result = queryTable(client, dataset_id, query)
    question_map = {}
    # count = 0
    for row in result:
        # if count > 10:
        #     break
        # count += 1
        v = list(row[1:])
        question_map[row[0]] = v
        # print("v: ", v)
    print("question map loaded")
    return question_map

question_vectors = load_question_vector()

@app.route('/hello')
def hello_world():
    return 'Hello, World!'

def getAnswer(qid):
    accepted_answer_query = ("""
        SELECT 
            accepted_answer_id
        FROM 
            `optical-metric-260620.stackoverflow.questions`
        WHERE
            qid = {};
    """).format(qid)
    result = queryTable(client, dataset_id, accepted_answer_query)
    accepted_answer_id = 0
    for row in result:
        accepted_answer_id = row[0]

    answer_query = ("""
        SELECT
            body
        FROM
            `optical-metric-260620.stackoverflow.answers`
        WHERE
            aid = {};
    """).format(accepted_answer_id)
    result = queryTable(client, dataset_id, answer_query)
    answer = ""
    for row in result:
        answer = row[0]
    return answer

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

    max = float('-inf')
    maxQid = 0
    for pid in question_vectors.keys():
        sim = vectorSimilarity(compressed_vector, question_vectors[pid])
        print("sim: ", sim)
        if sim > max:
            max = sim
            maxQid = pid

    print("maxQid is: ", maxQid)

    answer = getAnswer(maxQid)

    # TODO(zwen): go over saved trained vectors and calculate distance
    return answer + "\n"


if __name__ == '__main__':
    app.run()
