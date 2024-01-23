# %%

# Import necessary libraries
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from itertools import product
from sklearn import metrics

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dropout, GRU

num_classes = 12

# Set the path to the data directory
PATH = os.path.join('months_data')

# Create an array of actions (signs) labels by listing the contents of the data directory
actions = np.array(os.listdir(PATH))

# Define the number of sequences and frames
sequences = 30
frames = 40

# Create a label map to map each action label to a numeric value
label_map = {label:num for num, label in enumerate(actions)}

# Initialize empty lists to store landmarks and labels
landmarks, labels = [], []

# Iterate over actions and sequences to load landmarks and corresponding labels
for action, sequence in product(actions, range(sequences)):
    temp = []
    for frame in range(frames):
        npy = np.load(os.path.join(PATH, action, str(sequence), str(frame) + '.npy'))
        temp.append(npy)
    landmarks.append(temp)
    labels.append(label_map[action])

# Convert landmarks and labels to numpy arrays
X, Y = np.array(landmarks), to_categorical(labels).astype(int)

# Split the data into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.15, random_state=34, stratify=Y)

# Define the model architecture
model = Sequential()
# model.add(LSTM(32, return_sequences=True, activation='relu', input_shape=(frames,225)))
model.add(Conv1D(32, 3, padding='same', input_shape=(frames,225)))
model.add(Activation('relu'))
model.add(Conv1D(32, 3))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2))) 
model.add(Dropout(0.25))

model.add(Conv1D(64, 3, padding='same'))
model.add(Activation('relu'))
model.add(Conv1D(64, 3))
model.add(Activation('relu'))
model.add(MaxPooling1D(pool_size=(2)))
model.add(Dropout(0.25))

# Recurrent layers to integrate temporal information
model.add(GRU(64, return_sequences=True))  
model.add(GRU(32, return_sequences=False))

# Fully-connected layers    
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.4))
model.add(Dense(num_classes, activation='softmax'))
# model.add(Dense(actions.shape[0], activation='softmax'))

# Compile the model with Adam optimizer and categorical cross-entropy loss
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['categorical_accuracy'])

# Train the model
model.fit(X_train, Y_train, epochs=200)

# Save the trained model
model.save('months_model')

# Make predictions on the test set
predictions = np.argmax(model.predict(X_test), axis=1)
# Get the true labels from the test set
test_labels = np.argmax(Y_test, axis=1)

# Calculate the accuracy of the predictions
accuracy = metrics.accuracy_score(test_labels, predictions)
