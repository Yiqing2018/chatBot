import logging
from gensim.models.word2vec import LineSentence, Word2Vec


# turn on the logger
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# build model, save as w2v.mod
sentences= LineSentence("questions_for_word_vector.txt")
model = Word2Vec(sentences ,min_count=1, iter=1000)
model.train(sentences, total_examples=model.corpus_count, epochs=1000)
model.save("../model/w2v.mod")
print("Done with word2vec")

# test the model
# the most similar words with "web" should include "website"...

# model_loaded = Word2Vec.load("model/w2v.mod")
# sim = model_loaded.wv.most_similar(positive=['web'])
# for s in sim:
#     print (s[0])
