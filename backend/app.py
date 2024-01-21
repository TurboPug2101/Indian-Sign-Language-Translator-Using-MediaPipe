import asyncio
import threading
import os
import numpy as np
import cv2
import base64
import websockets
from flask import *
from flask_cors import CORS,cross_origin
from flask_socketio import SocketIO
from tensorflow.keras.models import load_model
import zipfile




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
print("CORS enabled for all domains")
@app.route('/')
def index():
    return jsonify({"Messgae":"This is the backend server"})

@app.route('/get_model')
def get_model():
    model_path = "D:\\Sign-Language-Translator\\models\\greetings_model.h5"  # Replace this with the actual path to your model file
    try:
        loaded_model = load_model(model_path)
        model_temp_path = 'temp_model.h5'
        loaded_model.save(model_temp_path)  # Save a temporary copy of the model
        return send_file(model_temp_path, as_attachment=True)
    except Exception as e:
        return f"Adarsh u have an Error: {str(e)}"
# Set the path to the data directory
PATH = os.path.join(r"D:\Sign-Language-Translator\greetings_data")

# Create an array of action labels by listing the contents of the data directory
actions = np.array(os.listdir(PATH))
@app.route('/load_data')
def load_data():
    return jsonify({'actions': actions.tolist()})


@app.route('/process_frame', methods=['POST'])
def process_frame():
    return 'Frame processed successfully'
@app.route('/texttosign', methods=['POST'])
@cross_origin()
def texttosign():
    if request.method == 'OPTIONS':
        # The response to the preflight OPTIONS request
        return '', 200
    sentences = request.json.get('sentences')
    sentences = sentences.upper().split()  
    PATH = "./data"
    all_words=os.listdir(PATH)
    valid_sentences = [sentence for sentence in sentences if sentence+".mp4" in all_words]
    video_files = [os.path.join(PATH, f"{sentence}.mp4") for sentence in valid_sentences]
    print(video_files)

    
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
