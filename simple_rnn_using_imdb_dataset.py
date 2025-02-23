# -*- coding: utf-8 -*-
"""Simple RNN using IMDB dataset

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1prIJtF4r49bNnQyegH6lxYTHpxvxSEN0
"""

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, SimpleRNN
from tensorflow.keras.datasets import imdb

# Load the IMDb dataset
max_features = 10000  # Vocabulary size
max_len = 500  # Maximum length of sequences
(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_features)
'''
1. Max_features is set to 10000, which represents the vocabulary size. This means that the dataset will only
 consider the 10000 most frequent words in the IMDB movie review dataset.
 Any words outside this vocabulary will be discarded.

2. max_len = 500 sets a maximum length of 500 for the movie reviews.'''

print(f'Training data shape: {X_train.shape}, Training labels shape:{y_train.shape}')
print(f'Testing data shape: {X_test.shape}, Testing labels shape:{y_train.shape}')

X_train[0],y_train[0]  ## these are the one hot representation of every word of x[0] and y[0].
# y[0] is tyypically 0 & 1 represnting positive and negative sentiment score

## Inspect sample review and its label
print(f'Sample review(as integers): {X_train[0]}')
print(f'Sample label: {y_train[0]}')

## Mapping of words index back to words(for understanding)
word_index= imdb.get_word_index()
#word_index
reverse_word_index = dict([(value, key) for (key, value) in word_index.items()])
reverse_word_index

# Decode the first review
word_index = imdb.get_word_index()
reverse_word_index = {value: key for key, value in word_index.items()}
decoded_review = ' '.join([reverse_word_index.get(i - 3, '?') for i in X_train[0]])
print(f'Decoded review: {decoded_review}')

# Pad sequences
X_train = sequence.pad_sequences(X_train, maxlen=max_len)
X_test = sequence.pad_sequences(X_test, maxlen=max_len)
X_train
'''
1. from tensorflow.keras.preprocessing import sequence imports the sequence module from Keras.
This module provides tools for preprocessing text data, including padding sequences.

2. X_train = sequence.pad_sequences(X_train, maxlen=max_len) and X_test = sequence.pad_sequences(X_test, maxlen=max_len)
apply padding to the training and testing data, respectively.

3. Padding: Movie reviews come in different lengths. For neural networks to process them efficiently, they need to be of uniform length.
Padding ensures this. Reviews shorter than max_len are padded with zeros at the beginning, while longer reviews are truncated.

4. sequence.pad_sequences: This function handles the padding process.
It takes the input sequences (X_train, X_test) and the desired maximum length (max_len) as arguments.

5. X_train at the end: This line simply displays the padded training data (X_train).
This is probably for inspection purposes, to see how the padding has affected the data.

In essence, cell 7 prepares the movie review data for input into a neural network by
ensuring all reviews have a consistent length of 500 through padding '''

# Define the RNN model
model = Sequential([
    Embedding(max_features, 32, input_length=max_len),  # Embedding layer
    SimpleRNN(32, activation='relu'),  # RNN layer
    Dense(1, activation='sigmoid')  # Output layer for binary classification
])
model.build(input_shape=(None, max_len))  # Build the model explicitly
model.summary()  # Verify the total number of parameters

# Print model summary to check total parameters
model.summary()

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2
)

from tensorflow.keras.layers import Dropout

model = Sequential([
          Embedding(max_features, 32, input_length=max_len),
          SimpleRNN(32, activation='relu'),
          Dropout(0.2),  # Dropout layer with a rate of 0.2
          Dense(1, activation='sigmoid')
      ])
model.build(input_shape=(None, max_len))
model.summary()

#Compile model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# Train the model

history = model.fit(
    X_train, y_train,
    epochs=20,
    batch_size=32,
    validation_split=0.2
)

## Save model file
model.save('simple_rnn_model.h5')

from tensorflow.keras.models import Sequential, load_model
 from tensorflow.keras.layers import Dense, Embedding, SimpleRNN
 from tensorflow.keras.datasets import imdb
 from tensorflow.keras.preprocessing.sequence import pad_sequences

#Load the pretrained model with ReLu activation
model = load_model('simple_rnn_model.h5')
model.summary()

model.get_weights()

# Helper Function
# Function to decode review
def decoded_review(encoded_review):
    return ' '.join([reverse_word_index.get(i-3, '?') for i in encoded_review])

# Function to preprocess user input
def preprocess_text(text):
  from tensorflow.keras.preprocessing import sequence # Import sequence here
  words =text.lower().split()
  encoded_review = [word_index.get(word,2)+3 for word in words]
  padded_review = sequence.pad_sequences([encoded_review], maxlen=500) # Now sequence is defined
  return padded_review

### Prediction function
def predict_sentiment(review):
  preprocessed_input = preprocess_text(review)

  prediction = model.predict(preprocessed_input)[0][0]
  sentiment = 'Positive' if prediction > 0.5 else 'Negative'
  return sentiment, prediction

# User input and Prediction
# Example review for prediction
example_review = "This movie was fantastic! The acting was great and plot was thrilling."
sentiment, prediction = predict_sentiment(example_review)
print(f"Sentiment: {sentiment}")
print(f"Prediction: {prediction}")

example_review2 = "This movie was not that great! One time watchable."
sentiment, prediction = predict_sentiment(example_review2)
print(f"Sentiment: {sentiment}")
print(f"Prediction: {prediction}")

example_review3 = "This movie was OK OK."
sentiment, prediction = predict_sentiment(example_review3)
print(f"Sentiment: {sentiment}")
print(f"Prediction: {prediction}")

example_review4 = "This movie is a blockbuster"
sentiment, prediction = predict_sentiment(example_review4)
print(f"Sentiment: {sentiment}")
print(f"Prediction: {prediction}")

