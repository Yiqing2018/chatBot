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
	dataset_id = "stackoverflow" # dataset_id used for query shouldn't contain project_id.
	query = """
	    SELECT id as qid, title, accepted_answer_id
		FROM `bigquery-public-data.stackoverflow.posts_questions`
		WHERE accepted_answer_id IS NOT NULL
		LIMIT 10;
	"""
	result = queryTable(client,dataset_id, query)
	result = cleanText(result)
	return result
	

	# Query from stackoverflow and save the result as answers table.
	# sql = """
	#     SELECT
	# 	  id as aid,
	# 	  body
	# 	FROM
	# 	  `bigquery-public-data.stackoverflow.posts_answers`
	# 	LIMIT 10;
	# """
	# queryTable(dataset_id, sql)



