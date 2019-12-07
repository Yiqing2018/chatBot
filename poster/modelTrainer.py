from preprocessor import loadQuestionsFromDB, load_vocabulary, preprocess
from autoencoder import AutoEncoder
from evaluate import eval
trainingPercent = 0.8

def main():
    data = loadQuestionsFromDB(100)
    print("Data loaded from DB.questions")

    # split training data and test data
    idx = int(len(data)*trainingPercent)
    trainingData = data[:idx]
    testingData = data[idx:]
    print("training data splitted")

    vocabulary = load_vocabulary(100)
    print("Vocabulary loaded and get the dictionary")

    cleanData, _ = preprocess(trainingData, vocabulary)
    print("Data preprocessed")

    # train model
    autoEncoder = AutoEncoder(cleanData)
    autoEncoder.run()

    # evaluation on testingData
    cleanData, _ = preprocess(testingData, vocabulary)
    print("Data preprocessed")
    eval(cleanData)
    

if __name__ == '__main__':
    main()