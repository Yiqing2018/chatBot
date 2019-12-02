import keras
from autoencoder import load_vocabulary, preprocess, loadQuestionsFromDB
from keras.models import load_model
from google.cloud import bigquery
import json

if __name__ == '__main__':
    # step1, save results into csv file
    # read all questions
    data = loadQuestionsFromDB(-1)
    vocabulary = load_vocabulary(-1)
    cleanedData, qids = preprocess(data, vocabulary)
    print("Data preprocessed")
    # write to a csv file with format (qid, compressed vector)
    encoder = load_model(r'./weights/encoder_weights.h5')
    encoded_vectors = keras.preprocessing.sequence.pad_sequences(
        cleanedData, 
        value=0, # 0 is for pad
        padding="post",
        maxlen=36)
    compressed_vectors = encoder.predict(encoded_vectors)
    with open('compressedVectors.csv', 'w') as f:
        for i in range(len(qids)):
            # print("compressed_vectors: ", compressed_vectors[i])
            f.write("%s,%s\n"%(qids[i],str(list(compressed_vectors[i]))[1:-1]))
        
    # step2, read results from csv file and save to DB

    # client = bigquery.Client()
    # filename = 'compressedVectors.csv'
    # dataset_id = 'stackoverflow'
    # table_id = 'compressed_vectors'
    # dataset_ref = client.dataset(dataset_id)
    # table_ref = dataset_ref.table(table_id)
    # job_config = bigquery.LoadJobConfig()
    # job_config.source_format = bigquery.SourceFormat.CSV
    # job_config.skip_leading_rows = 1
    # job_config.autodetect = True
    # with open(filename, "rb") as source_file:
    #     job = client.load_table_from_file(source_file, table_ref, job_config=job_config)
    # job.result()  # Waits for table load to complete.
    # print("Loaded {} rows into {}:{}.".format(job.output_rows, dataset_id, table_id))