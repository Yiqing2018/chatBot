import keras
from autoencoder import load_vocabulary, preprocess
from keras.models import load_model
from google.cloud import bigquery
import json

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
    query = """
    SELECT
        *
    FROM
        `optical-metric-260620.stackoverflow.questions`;
    """
    result = queryTable(client,dataset_id, query)
    return result

if __name__ == '__main__':
    # # read all questions
    # data = loadQuestionsFromDB()
    # vocabulary = load_vocabulary()
    # cleanedData, qids = preprocess(data, vocabulary)
    # print("Data preprocessed")

    # # write to a csv file with format (qid, compressed vector)
    # encoder = load_model(r'./weights/encoder_weights.h5')
    # encoded_vectors = keras.preprocessing.sequence.pad_sequences(
    #     cleanedData, 
    #     value=0, # 0 is for pad
    #     padding="post",
    #     maxlen=36)
    # compressed_vectors = encoder.predict(encoded_vectors)

    # # result = []
    # # for i in range(len(qids)):
    # #     # f.write("{},{}\n".format(qids[i],list(compressed_vectors[i])))
    # #     result.append({'qid': qids[i], 'vector': list(compressed_vectors[i])})
    # with open('ctest.csv', 'w') as f:
    #     count = 0
    #     for i in range(len(qids)):
    #         if count > 10:
    #             break
    #         count += 1
    #         print("compressed_vectors: ", compressed_vectors[i])
    #         f.write("%s,%s\n"%(qids[i],str(list(compressed_vectors[i]))[1:-1]))
        

    # save csv file to database
    client = bigquery.Client()
    filename = 'compressedVectors.csv'
    dataset_id = 'stackoverflow'
    table_id = 'compressed_vectors'

    dataset_ref = client.dataset(dataset_id)
    table_ref = dataset_ref.table(table_id)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    job_config.skip_leading_rows = 1
    job_config.autodetect = True

    with open(filename, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()  # Waits for table load to complete.

    print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))