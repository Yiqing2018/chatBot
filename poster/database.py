from google.cloud import bigquery

def queryAndSaveTable(dataset_id, sql, new_table_name):
	job_config = bigquery.QueryJobConfig()
	table_ref = client.dataset(dataset_id).table(new_table_name)
	job_config.destination = table_ref
	query_job = client.query(
	    sql,
	    location='US',
	    job_config=job_config)
	query_job.result()  # Waits for the query to finish
	print('Query results loaded to table {}'.format(table_ref.path))

if __name__ == '__main__':
	# Create a dataset which holds questions and answers tables.
	client = bigquery.Client()
	dataset_id = "{}.stackoverflow".format(client.project)
	print("dataset_id: ", dataset_id)
	dataset = bigquery.Dataset(dataset_id)
	dataset.location = "US"
	dataset = client.create_dataset(dataset)
	print("Created dataset {}.{}".format(client.project, dataset.dataset_id))

	dataset_id = "stackoverflow" # dataset_id used for query shouldn't contain project_id.
    # Query from stackoverflow and save the result as questions table.
	sql = """
	    SELECT
		  id as qid,
		  title,
		  accepted_answer_id
		FROM
		  `bigquery-public-data.stackoverflow.posts_questions`
		WHERE
		  accepted_answer_id IS NOT NULL;
	"""
	queryAndSaveTable(dataset_id, sql, "questions")

	# Query from stackoverflow and save the result as answers table.
	sql = """
	    SELECT
		  id as aid,
		  body
		FROM
		  `bigquery-public-data.stackoverflow.posts_answers`;
	"""
	queryAndSaveTable(dataset_id, sql, "answers")



