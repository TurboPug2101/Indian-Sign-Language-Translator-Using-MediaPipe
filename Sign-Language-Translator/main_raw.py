# Import necessary libraries
import numpy as np
import os
import string
import mediapipe as mp
import cv2
from my_functions import *
import keyboard
from tensorflow.keras.models import load_model
import pyttsx3


# Set the path to the data directory
PATH = os.path.join('months_data')

# Create an array of action labels by listing the contents of the data directory
actions = np.array(os.listdir(PATH))

# Load the trained model
model = load_model('months_model')

# Initialize the lists
sentence, keypoints, last_prediction = [], [], []

engine = pyttsx3.init()

# Access the camera and check if the camera is opened successfully
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Cannot access camera.")
    exit()

# Create a holistic object for sign prediction
with mp.solutions.holistic.Holistic(min_detection_confidence=0.75, min_tracking_confidence=0.75) as holistic:
    # Run the loop while the camera is open
    while cap.isOpened():
        # Read a frame from the camera
        _, image = cap.read()
        # Process the image and obtain sign landmarks using image_process function from my_functions.py
        results = image_process(image, holistic)
        # Draw the sign landmarks on the image using draw_landmarks function from my_functions.py
        draw_landmarks(image, results)
        # Extract keypoints from the pose landmarks using keypoint_extraction function from my_functions.py
        keypoints.append(keypoint_extraction(results))

        # Check if frames have been accumulated
        if len(keypoints) ==40:
            # Convert keypoints list to a numpy array
            keypoints = np.array(keypoints)
            # Make a prediction on the keypoints using the loaded mosdel
            prediction = model.predict(keypoints[np.newaxis, :, :])
            # Clear the keypoints list for the next set of frames
            keypoints = []

            # Check if the maximum prediction value is above 0.8
            if np.amax(prediction) > 0.85:
                # Check if the predicted sign is different from the previously predicted sign
                if last_prediction != actions[np.argmax(prediction)]:
                    # Append the predicted sign to the sentence list
                    sentence.append(actions[np.argmax(prediction)])

                     # Read aloud the predicted word
                    engine.say(actions[np.argmax(prediction)])
                    engine.runAndWait()
                    
                    # Record a new prediction to use it on the next cycle
                    last_prediction = actions[np.argmax(prediction)]

        # Limit the sentence length to 7 elements to make sure it fits on the screen
        if len(sentence) > 5:
            sentence = sentence[-5:]

        if keyboard.is_pressed('enter'):
            # Append the sentence to the text file
            with open('predicted_sentences.txt', 'a') as file:
                file.write(' '.join(sentence) + '\n')
            # Clear the sentence for the next set of predictions
            sentence = []

        # Reset if the "Spacebar" is pressed
        if keyboard.is_pressed(' '):
            sentence, keypoints, last_prediction = [], [], []

        # Check if the list is not empty
        if sentence:
            # Capitalize the first word of the sentence
            sentence[0] = sentence[0].capitalize()

        # Check if the sentence has at least two elements
        if len(sentence) >= 2:
            # Check if the last element of the sentence belongs to the alphabet (lower or upper cases)
            if sentence[-1] in string.ascii_lowercase or sentence[-1] in string.ascii_uppercase:
                # Check if the second last element of sentence belongs to the alphabet or is a new word
                if sentence[-2] in string.ascii_lowercase or sentence[-2] in string.ascii_uppercase or (sentence[-2] not in actions and sentence[-2] not in list(x.capitalize() for x in actions)):
                    # Combine last two elements
                    sentence[-1] = sentence[-2] + sentence[-1]
                    sentence.pop(len(sentence) - 2)
                    sentence[-1] = sentence[-1].capitalize()

        # Calculate the size of the text to be displayed and the X coordinate for centering the text on the image
        textsize = cv2.getTextSize(' '.join(sentence), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
        text_X_coord = (image.shape[1] - textsize[0]) // 2

        # Draw the sentence on the image
        for i, word in enumerate(sentence):
            color = (0, 255, 0) if i == len(sentence) - 1 else (255, 255, 255)
            cv2.putText(image, word, (text_X_coord, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)
            text_X_coord += cv2.getTextSize(word, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0][0] + 10  # Add space between words


        # Show the image on the display
        cv2.imshow('Camera', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break


        # # Check if the 'Camera' window was closed and break the loop
        # if cv2.getWindowProperty('Camera',cv2.WND_PROP_VISIBLE) < 1:
        #     break

    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()
