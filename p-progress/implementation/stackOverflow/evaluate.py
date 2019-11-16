# pip install git+https://github.com/abenassi/Google-Search-API
from google import google

num_page = 1
search_results = google.search("string split java site stackoverflow", num_page)
if len(search_results) > 0:
	result = search_results[0]
	title = result.name
	if len(title.split("-")) > 0:
		print("result from google:",title.split("-")[0])
		print("external link:",result.link)