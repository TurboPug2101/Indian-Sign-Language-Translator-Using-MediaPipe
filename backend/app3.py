# import asyncio
# import threading
import os
# import numpy as np
# import cv2
# import base64
# import websockets as ws 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk
from flask import *
from flask_cors import CORS,cross_origin
from flask_socketio import SocketIO
# from keras.models import load_model
import zipfile

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
print("CORS enabled for all domains")

@app.route('/')
def index():
    return jsonify({"Messgae":"This is the backend server"})

# @app.route('/get_model')
# def get_model():
#     model_path = "D:\\Sign-Language-Translator\\models\\greetings_model.h5"  # Replace this with the actual path to your model file
#     try:
#         loaded_model = load_model(model_path)
#         model_temp_path = 'temp_model.h5'
#         loaded_model.save(model_temp_path)  # Save a temporary copy of the model
#         return send_file(model_temp_path, as_attachment=True)
#     except Exception as e:
#         return f"Adarsh u have an Error: {str(e)}"
# Set the path to the data directory
#PATH = os.path.join(r"D:\Sign-Language-Translator\greetings_data")

# Create an array of action labels by listing the contents of the data directory
#actions = np.array(os.listdir(PATH))
# @app.route('/load_data')
# def load_data():
#     return jsonify({'actions': actions.tolist()})


@app.route('/process_frame', methods=['POST'])
def process_frame():
    return 'Frame processed successfully'

@app.route('/texttosign', methods=['POST'])
@cross_origin()
def texttosign():
    if request.method == 'OPTIONS':
        # The response to the preflight OPTIONS request
        return '', 200
    
    text = request.json.get('sentences')
    print(text)
    text = text.upper()
    # tokenizing the sentence
    words = word_tokenize(text)
    tagged = nltk.pos_tag(words)
    tense = {}
    tense["future"] = len([word for word in tagged if word[1] == "MD"])
    tense["present"] = len([word for word in tagged if word[1] in ["VBP", "VBZ", "VBG"]])
    tense["past"] = len([word for word in tagged if word[1] in ["VBD", "VBN"]])
    tense["present_continuous"] = len([word for word in tagged if word[1] in ["VBG"]])

    # stopwords that will be removed
    stop_words = set(
        ["mightn't", 're', 'wasn', 'wouldn', 'be', 'has', 'that', 'does', 'shouldn', 'do', "you've", 'off', 'for',
            "didn't", 'm', 'ain', 'haven', "weren't", 'are', "she's", "wasn't", 'its', "haven't", "wouldn't", 'don',
            'weren', 's', "you'd", "don't", 'doesn', "hadn't", 'is', 'was', "that'll", "should've", 'a', 'then', 'the',
            'mustn', 'i', 'nor', 'as', "it's", "needn't", 'd', 'am', 'have', 'hasn', 'o', "aren't", "you'll",
            "couldn't", "you're", "mustn't", 'didn', "doesn't", 'll', 'an', 'hadn', 'whom', 'y', "hasn't", 'itself',
            'couldn', 'needn', "shan't", 'isn', 'been', 'such', 'shan', "shouldn't", 'aren', 'being', 'were', 'did',
            'ma', 't', 'having', 'mightn', 've', "isn't", "won't"])

    # removing stopwords and applying lemmatizing nlp process to words
    lr = WordNetLemmatizer()
    filtered_text = []
    for w, p in zip(words, tagged):
        if w not in stop_words:
            if p[1] == 'VBG' or p[1] == 'VBD' or p[1] == 'VBZ' or p[1] == 'VBN' or p[1] == 'NN':
                filtered_text.append(lr.lemmatize(w, pos='v'))
            elif p[1] == 'JJ' or p[1] == 'JJR' or p[1] == 'JJS' or p[1] == 'RBR' or p[1] == 'RBS':
                filtered_text.append(lr.lemmatize(w, pos='a'))

            else:
                filtered_text.append(lr.lemmatize(w))

    # adding the specific word to specify tense
    words = filtered_text
    temp = []
    for w in words:
        if w == 'Me':
            temp.append('I')
        else:
            temp.append(w)
    words = temp
    
    # probable_tense = max(tense, key=tense.get)
    #  if probable_tense == "past" and tense["past"] >= 1:
    #         temp = ["Before"]
    #         temp = temp + words
    #         words = temp
    #     elif probable_tense == "future" and tense["future"] >= 1:
    #         if "Will" not in words:
    #             temp = ["Will"]
    #             temp = temp + words
    #             words = temp
    #         else:
    #             pass
    #     elif probable_tense == "present":
    #         if tense["present_continuous"] >= 1:
    #             temp = ["Now"]
    #             temp = temp + words
    #             words = temp

    # filtered_text = []
    # for w in words:
    #     path = w + ".mp4"
    #     f = finders.find(path)
    #     # splitting the word if its animation is not present in database
    #     if not f:
    #         for c in w:
    #             filtered_text.append(c)
    #     # otherwise animation of word
    #     else:
    #         filtered_text.append(w)
    # words = filtered_text
    
    PATH = "./data"
    all_words=os.listdir(PATH)
    
    print(words)
    valid_sentences = [sentence for sentence in words if sentence+".mp4" in all_words]
    print(valid_sentences)
    video_files = [os.path.join(PATH, f"{sentence}.mp4") for sentence in valid_sentences]
    
    for video_file in video_files:
        if not os.path.isfile(video_file):
            return f'Video file {video_file} not found', 404

    # Send video files as a zip archive
    return send_file(zip_video_files(video_files), mimetype='application/zip', as_attachment=True)
    return f'The data is {sentences} and the video path is {video_files}'

def zip_video_files(video_files):
    zip_filename = 'videos.zip'
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for video_file in video_files:
            zipf.write(video_file, os.path.basename(video_file))
    return zip_filename
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

if (__name__=='__main__'):
    socketio.run(app,debug=True,port=5050,allow_unsafe_werkzeug=True)
