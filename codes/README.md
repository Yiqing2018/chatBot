# file structure

## population
#### prepareData.py  
clean the original dataset, populate to server. saved as two tables:  
bigquery-public-data.stackoverflow.posts_questions  
bigquery-public-data.stackoverflow.posts_answers  
#### vocabuilder.py
build vocabulary dictionary and populate to server
#### vocabulary.py
populate vocabulary.csv to server

## training the model
#### preprocessor.py
querying the database and get clean data with vocabulary dict
#### autoencoder.py
build NN model  
#### modelTrainer.py
training the model  
#### encode.py
compute the vector all questions in DB

## interface
#### app.py 

## results & conclusion
#### evaluate.py  
loading the built model, apply to test data, to see the performance of autoencoder  
#### analyze.py  
analyzing the experiment result, draw some pictures  
