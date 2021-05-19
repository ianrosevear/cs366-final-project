import numpy as np
import pandas as pd
from tensorflow.python.keras.preprocessing.text import Tokenizer
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Embedding, LSTM, GRU
from keras.layers.embeddings import Embedding

def eval_riddles(file):

    #load data
    df_train = pd.read_csv("TRAINING_CLEAN.csv", sep=',')
    df_test = pd.read_csv("TESTING_CLEAN.csv", sep=',')

    #split data into Riddle and score
    R_train = df_train.loc[0:, "riddle"].values
    s_train = df_train.loc[0:, "score"].values
    R_test = df_test.loc[0:, "riddle"].values
    s_test = df_test.loc[0:, "score"].values

    for i, x in enumerate(s_train):
        if x >= 2:
            s_train[i] = 1
        else:
            s_train[i] = 0

    for i, x in enumerate(s_test):
        if x >= 2:
            s_train[i] = 1
        else:
            s_train[i] = 0

    #tokenize data
    tokenizer_obj = Tokenizer()
    total_riddles = np.concatenate((R_train, R_test))
    tokenizer_obj.fit_on_texts(total_riddles)

    #pad sequences to make them same length
    max_length = max([len(s.split()) for s in total_riddles])

    #define vocabulary size
    vocab_size = len(tokenizer_obj.word_index) + 1

    #create tokens
    R_train_tokens = tokenizer_obj.texts_to_sequences(R_train)
    R_test_tokens = tokenizer_obj.texts_to_sequences(R_test)

    R_train_pad = pad_sequences(R_train_tokens, maxlen=max_length, padding="post")
    R_test_pad = pad_sequences(R_test_tokens, maxlen=max_length, padding="post")

    #make embedding layer
    EMBEDDING_DIM = 50

    print("Building optimization model...")

    model = Sequential()
    model.add(Embedding(vocab_size, EMBEDDING_DIM, input_length = max_length))
    model.add(GRU(units = 32, dropout = 0.2, recurrent_dropout = 0.2))
    model.add(Dense(1, activation="sigmoid"))

    #try using different optimizers and different optimizer configs
    model.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"])

    #train model
    print("Training optimization model...")
    model.fit(R_train_pad, s_train, batch_size=15, epochs=3,
              validation_data=(R_test_pad, s_test), verbose=2)

    best_riddles = []
    with open(file) as f:
        for line in f:
            line = eval(line)
            riddle_tokens = tokenizer_obj.texts_to_sequences(line)
            riddle_tokens_pad = pad_sequences(riddle_tokens, maxlen=max_length)
            scores = model.predict(x=riddle_tokens_pad)

            best = line[np.argmax(line)]
            best_riddles.append(best)

    return best_riddles



# #test model
# test_a1 = "What is related to attribute/ but isn't related to account book/? quality/!"
# test_b1 = "What is related to visitation/ but isn't related to canonical/? visit/!"
# test_c0 = "What is found at bedroom/ but isn't found at furniture store/? house/!"
# test_d2 = "What is found at university/ but can't seat many people/? education/!"
# test_e0 = "Sorry, we can't make a very good riddle with this startword."
# test_f3 = "What is related to aids/ but isn't related to acquired immune deficiency syndrome/? aid/!"
#
# test_samples = [test_a1, test_b1, test_c0, test_d2, test_e0, test_f3]
# test_samples_tokens = tokenizer_obj.texts_to_sequences(test_samples)
# test_samples_tokens_pad = pad_sequences(test_samples_tokens, maxlen=max_length)
#
# #predict
# model.predict(x=test_samples_tokens_pad)
#
# #evaluate
# #model.evaluate(x=R_test_pad, y=s_test)
