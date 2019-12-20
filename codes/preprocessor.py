from google.cloud import bigquery
import keras
import string
import numpy as np
import autoencoder

maxlen = autoencoder.maxlen

# tokenizes and preprocess a question, removing all punctuation, convert to lower case
def cleanQuestion(question):
    q = question.translate(str.maketrans('', '', string.punctuation)).lower()
    words = q.split()
    return words

def queryTable(client, dataset_id, sql):
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(
        sql,
        location='US',
        job_config=job_config)
    return query_job.result()  # Waits for the query to finish

# @limitedSize: 
# -1: unlimited, extracting all data
# [1, dataset_size]: select part of data
def loadQuestionsFromDB(limitedSize):
    client = bigquery.Client()
    dataset_id = "stackoverflow" # dataset_id used for query shouldn't contain project_id.
    if limitedSize != -1:
        query = """
        SELECT
            *
        FROM
            `optical-metric-260620.stackoverflow.questions`
        LIMIT {};
        """.format(limitedSize)
    else:
        query = """
        SELECT
            *
        FROM
            `optical-metric-260620.stackoverflow.questions`;
        """
    result_from_db = queryTable(client,dataset_id, query)
    result = []
    for row in result_from_db:
        result.append(row)
    return result

# @limitedSize: 
# -1: unlimited, extracting all data
# [1, dataset_size]: select part of data
def load_vocabulary(limitedSize):
    client = bigquery.Client()
    dataset_id = "stackoverflow"
    if limitedSize != -1:
        query = """
            SELECT 
                *
            FROM 
                `optical-metric-260620.stackoverflow.vocabulary`
            LIMIT {};
        """.format(limitedSize)
    else:
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

# @data: the data extracted from server
# @vocabulary: using vocabulary dictionary to process text input
def preprocess(data, vocabulary):
    trainingData = []
    count = 0
    qids = []
    for row in data:
        sample = []
        words = cleanQuestion(row[1])
        for word in words:
            if word in vocabulary:
                sample.append(vocabulary[word])
            else:
                sample.append(1) # 1 is for unknown
        # normalize the vector
        sample = normalizeVector(sample)
        trainingData.append(sample)
        qids.append(row[0])
    trainingData = keras.preprocessing.sequence.pad_sequences(
        trainingData, 
        value=0.0, # 0 is for pad
        padding="post",
        dtype='float32',
        maxlen=maxlen)
    return trainingData, qids

def normalizeVector(x):
    x=np.array(x)
    y=np.linalg.norm(x, ord = 2, keepdims=True) # ord : norm dimension
    return (x/y).tolist()

def generate_initial_vector(words, vocabulary):
    sample = []
    for word in words:
        if word in vocabulary:
            sample.append(vocabulary[word])
        else:
            sample.append(1) # 1 is for unknown
    return sample