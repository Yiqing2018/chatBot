# A Chatbot Based on Stackoverflow


## Introduction
when users are trying to find answers to a specific question online, they usually would get lots of relevant information, which is overwhelming. Sometimes it is challenging to find the best answer, especially for new beginners. Our goal is to build a chatbot, which could find the best matched question with the user query and return the top rated answer of that question as answer to user query. This will save users' efforts for information filtering.
The underlying idea is to compute text similarity between user input and existing questions in our database

## Problem Definition
input: the sentence from user input  

For example: How to import package in Python?  

output: the top-rated answer of the best matched question according to user input  

underlying problem: implement an approach to compute the similarity between input text and questions stored in DB efficiently  

dataset: [StackOverflow Data from kaggle](https://www.kaggle.com/stackoverflow/stackoverflow)  
StackOverflow is one of the largest online community for programmers to learn, share their knowledge.  
After data cleaning, we would mainly use two tables:  
questions: question_id, question_title, top_rated_answer_id  
answers: answer_id, answer_content
![](http://ww2.sinaimg.cn/large/006tNbRwly1ga2y4se0bxj311k0a0tae.jpg)

## Approaches
AutoEncoder: is a type of artificial neural network, and it is used to learn data in an unsupervised manner. It would help find out a good representation of input big data, and usually compressed to a smaller dataset - which is encoding process. And this compressed data could be decompressed to the output data - which is decoding process.
If the original dataset is similar with the output dataset, it means the AutoEncoder could represent the input data quite well.

## Infrastructure
In our project, our goal is to find the intermediate result - function h, to represent the data from input layer.
To be specific, we implemented an AutoEncoder for compressing the user input sentence to a short vector and use that representation to compute the similarity between two sentences.
Once we found the most similar question in the database, the program would return the top-rated answer of that question.

the similarity of two vectors are measured in the following way:
similarity Score(vector1, vector2) = cos(x) = (vector1*vector2)/(|vector1| |vector2|)

the more similar, the cos(x) is more close to 1

dependencies:  
language: Python3  
packages: tensorflow, keras  
data storage: BigQuery from Google Cloud  
## Interface
![](http://ww4.sinaimg.cn/large/006tNbRwly1ga2yf58y79j320i0eewsl.jpg)
##  Testing results
Testing on 20% of full dataset, the average similarity score is 0.476496
Training model on different datasize, evaluate its performance and  running time
the performance of different data size
1.the performance of different data size  
![](http://ww4.sinaimg.cn/large/006tNbRwly1ga2y9hp2ilj30vy0awta1.jpg)
2.running time, on different data set
![](http://ww1.sinaimg.cn/large/006tNbRwly1ga2y9wdxkgj30y80a6ab9.jpg)
it’s running very fast on small size data, no more than 1 minute, but on the whole dataset, it runs for almost 50 minutes
##  References
Yao, L., Pan, Z., & Ning, H. (2018). Unlabeled Short Text Similarity With LSTM Encoder. IEEE Access, 7, 3430-3437.  
Seo, M., Kembhavi, A., Farhadi, A., & Hajishirzi, H. (2016). Bidirectional attention flow for machine comprehension. arXiv preprint arXiv:1611.01603.  
Devlin, J., Chang, M. W., Lee, K., & Toutanova, K. (2018). Bert: Pre-training of deep bidirectional transformers for language understanding. arXiv preprint arXiv:1810.04805.   
Wang, S., & Jiang, J. (2015). Learning natural language inference with LSTM. arXiv preprint arXiv:1512.08849.  
Wang, S., & Jiang, J. (2016). Machine comprehension using match-lstm and answer pointer. arXiv preprint arXiv:1608.07905.  




