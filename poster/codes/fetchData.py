from google.cloud import bigquery
import os
import string


def queryTable(client, dataset_id, sql):
	job_config = bigquery.QueryJobConfig()
	query_job = client.query(
	    sql,
	    location='US',
	    job_config=job_config)
	return query_job.result()  # Waits for the query to finish

def cleanText(result):
	cleanResult = list()
	for row in result:
		sample = list()
		sample.append(row[0])
		sample.append(
			row[1].translate(str.maketrans('', '', string.punctuation)).lower())
		sample.append(row[2])
		cleanResult.append(sample)
	return cleanResult


def getData():
	client = bigquery.Client()
	dataset_id = "stackoverflow"
	query = """
		SELECT *
		FROM `optical-metric-260620.stackoverflow.questions`
		LIMIT 10000;
	"""
	result = queryTable(client,dataset_id, query)
	result = cleanText(result)
	return result



