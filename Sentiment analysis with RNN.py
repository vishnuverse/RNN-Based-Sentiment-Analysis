
# We will use Recurrent Neural Networks, and in particular LSTMs, to perform sentiment analysis in Keras.  Conveniently, Keras has a built-in IMDb movie reviews dataset that we can use.
from keras.datasets import imdb

vocabulary_size = 5000

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words = vocabulary_size)
print('Loaded dataset with {} training samples, {} test samples'.format(len(X_train), len(X_test)))


#  Inspect a sample review and its label


print('---review---')
print(X_train[6])
print('---label---')
print(y_train[6])


# Map word IDs back to words


word2id = imdb.get_word_index()
id2word = {i: word for word, i in word2id.items()}
print('---review with words---')
print([id2word.get(i, ' ') for i in X_train[6]])
print('---label---')
print(y_train[6])


# Maximum review length and minimum review length

print('Maximum review length: {}'.format(len(max((X_train + X_test), key=len))))

print('Minimum review length: {}'.format(len(min((X_test + X_test), key=len))))

# ### Pad sequences
# 
# In order to feed this data into our RNN, all input documents must have the same length. We will limit the maximum review length to max_words by truncating longer reviews and padding shorter reviews with a null value (0). We can accomplish this using the pad_sequences() function in Keras. For now, set max_words to 500.


from keras.preprocessing import sequence

max_words = 500
X_train = sequence.pad_sequences(X_train, maxlen=max_words)
X_test = sequence.pad_sequences(X_test, maxlen=max_words)


# ### TODO: Design an RNN model for sentiment analysis
# 
# Build our model architecture in the code cell below. We have imported some layers from Keras that you might need but feel free to use any other layers / transformations you like.
# 
# Remember that our input is a sequence of words (technically, integer word IDs) of maximum length = max_words, and our output is a binary sentiment label (0 or 1).


from keras import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout

embedding_size=32
model=Sequential()
model.add(Embedding(vocabulary_size, embedding_size, input_length=max_words))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))

print(model.summary())


# To summarize, our model is a simple RNN model with 1 embedding, 1 LSTM and 1 dense layers. 213,301 parameters in total need to be trained.

# ### Train and evaluate our model
# 
# We first need to compile our model by specifying the loss function and optimizer we want to use while training, as well as any evaluation metrics we'd like to measure. Specify the approprate parameters, including at least one metric 'accuracy'.


model.compile(loss='binary_crossentropy',  optimizer='adam', metrics=['accuracy'])


# Once compiled, we can kick off the training process. There are two important training parameters that we have to specify - batch size and number of training epochs, which together with our model architecture determine the total training time.
# 
# Training may take a while, so grab a cup of coffee, or better, go for a run!


batch_size = 64
num_epochs = 3

X_valid, y_valid = X_train[:batch_size], y_train[:batch_size]
X_train2, y_train2 = X_train[batch_size:], y_train[batch_size:]

model.fit(X_train2, y_train2, validation_data=(X_valid, y_valid), batch_size=batch_size, epochs=num_epochs)

# scores[1] will correspond to accuracy if we pass metrics=['accuracy']

scores = model.evaluate(X_test, y_test, verbose=0)
print('Test accuracy:', scores[1])






