import string
import numpy as np
from google.cloud import bigquery
import csv

def cleanQuestion(question):
    """
    This method tokenizes and preprocess a question.
    """
    q = question.translate(str.maketrans('', '', string.punctuation)).lower()
    words = q.split()
    return words

def buildVocabulary(query_results):
    """
    This method receives a BigQuery query result with each row as [qid, question, answer_id], 
    iterates over the rows, and build a vocabulary.
    """
    vocabulary_list = []
    maxLen = 0
    for row in query_results:
        question_title = row[1] # row[0] is qid, row[2] is accepted_answer_id
        tokenized_question_title = cleanQuestion(question_title)
        maxLen = max(maxLen, len(tokenized_question_title))
        vocabulary_list.extend(tokenized_question_title)

    print("maxLen should be: ", maxLen)
    vocabulary = {k:(v + 2) for v, k in enumerate(np.unique(vocabulary_list))}
    vocabulary['<PAD>'] = 0
    vocabulary['<UNK>'] = 1
    print("There are ", len(vocabulary), " words in the vocabulary")
    return vocabulary

def queryTable(client, dataset_id, sql):
    job_config = bigquery.QueryJobConfig()
    query_job = client.query(
        sql,
        location='US',
        job_config=job_config)
    return query_job.result()  # Waits for the query to finish

if __name__ == '__main__':
    client = bigquery.Client()
    dataset_id = "stackoverflow"
    query = """
        SELECT 
            *
        FROM 
            `optical-metric-260620.stackoverflow.questions`;
    """
    result = queryTable(client, dataset_id, query)
    print("Query Finished")
    vocabulary = buildVocabulary(result)

    with open('vocabulary.csv', 'w') as f:
        for key in vocabulary.keys():
            f.write("%s,%s\n"%(key,vocabulary[key]))
