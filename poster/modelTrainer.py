from preprocessor import loadQuestionsFromDB, load_vocabulary, preprocess
from autoencoder import AutoEncoder
from evaluate import eval
trainingPercent = 0.8

def main():
    data = loadQuestionsFromDB(-1)
    print("Data loaded from DB.questions")

    # split training data and test data
    idx = int(len(data)*trainingPercent)
    trainingData = data[:idx]
    testingData = data[idx:]
    print("training data splitted")

    vocabulary = load_vocabulary(-1)
    print("Vocabulary loaded and get the dictionary")

    cleanData, _ = preprocess(trainingData, vocabulary)
    print("trainingData preprocessed")
    autoEncoder = AutoEncoder(cleanData)
    autoEncoder.run()
    print("model training done")


    # # evaluation on testingData
    # cleanData, _ = preprocess(testingData, vocabulary)
    # print("testiData preprocessed")
    # eval(cleanData)
    

if __name__ == '__main__':
    main()