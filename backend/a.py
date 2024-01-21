import asyncio
import threading
import os
import numpy as np
import cv2
import base64
import websockets
from flask import *
from flask_cors import CORS
from flask_socketio import SocketIO
from tensorflow.keras.models import load_model




app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")
print("CORS enabled for all domains")
@app.route('/')
def index():
    return jsonify({"Messgae":"This is the backend server"})

@app.route('/<name>')
def print_name(name):
    return jsonify({"output":f"Hi {name}. How are you doing ?"})

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

# async def handle_frame(websocket, path):
#     while True:
#         try:
#             # Receive image data from the WebSocket
#             image_data = await websocket.recv()

#             # Decode base64 and convert to NumPy array
#             image_bytes = base64.b64decode(image_data.split(',')[1])
#             nparr = np.frombuffer(image_bytes, np.uint8)
#             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             # Process the frame (You can replace this with your own processing logic)
#             # For example, you can save the frame to a file or perform some image processing
#             cv2.imshow('Received Frame', frame)
#             cv2.waitKey(1)

#         except websockets.exceptions.ConnectionClosed:
#             break
# start_server = websockets.serve(handle_frame, "localhost", 5000)
# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()




@app.route('/process_frame', methods=['POST'])
def process_frame():
    frame_data = request.json.get('frameData')  # Get frame data from the request
    # Process the received frame data (perform image processing or any required action)
    # Your processing logic here
    
    # Return a response if needed
    return 'Frame processed successfully'
@app.route('/texttosign',methods=['POST'])
def texttosign():
    sentences = request.json.get('sentences')
    sentences=sentences.split()
    nWords = len(sentences)
    return f'The data is {sentences}'
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

async def handle_frame(websocket, path):
    while True:
        try:
            # Receive image data from the WebSocket
            image_data = await websocket.recv()

            # Decode base64 and convert to NumPy array
            # image_bytes = base64.b64decode(image_data.split(',')[1])
            # nparr = np.frombuffer(image_bytes, np.uint8)
            # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Process the frame (You can replace this with your own processing logic)
            # For example, you can save the frame to a file or perform some image processing
            # cv2.imshow('Received Frame', frame)
            # cv2.waitKey(1)
            print("Received Frame")

        except websockets.exceptions.ConnectionClosed:
            break
# def start_websocket_server():
#     loop = asyncio.new_event_loop()
#     asyncio.set_event_loop(loop)
#     start_server = websockets.serve(handle_frame, "localhost", 5000)
#     loop.run_until_complete(start_server)
#     loop.run_forever()


if (__name__=='__main__'):
    # Start both Flask and SocketIO servers
    # threading.Thread(target=start_websocket_server).start()
    # socketio.run(app, debug=True, use_reloader=False, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)
    socketio.run(app,debug=True,port=5050,allow_unsafe_werkzeug=True)





# import asyncio
# import websockets
# import base64
# import numpy as np
# import os
# from flask import Flask, send_file, jsonify, request
# from flask_cors import CORS
# from tensorflow.keras.models import load_model
# import cv2  # Add this import statement for OpenCV

# async def handle_frame(websocket, path):
#     while True:
#         try:
#             # Receive image data from the WebSocket
#             image_data = await websocket.recv()

#             # Decode base64 and convert to NumPy array
#             image_bytes = base64.b64decode(image_data.split(',')[1])
#             nparr = np.frombuffer(image_bytes, np.uint8)
#             frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#             # Process the frame (You can replace this with your own processing logic)
#             # For example, you can save the frame to a file or perform some image processing
#             cv2.imshow('Received Frame', frame)
#             cv2.waitKey(1)

#         except websockets.exceptions.ConnectionClosed:
#             break

# start_server = websockets.serve(handle_frame, "localhost", 3000)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

# app = Flask(__name__)
# CORS(app)

# @app.route('/')
# def index():
#     return 'Hello, this is your backend!'

# @app.route('/get_model')
# def get_model():
#     model_path = "D:\\Sign-Language-Translator\\models\\greetings_model.h5"  # Replace this with the actual path to your model file
#     try:
#         loaded_model = load_model(model_path)
#         model_temp_path = 'temp_model.h5'
#         loaded_model.save(model_temp_path)  # Save a temporary copy of the model
#         return send_file(model_temp_path, as_attachment=True)
#     except Exception as e:
#         return f"Error: {str(e)}"

# # Set the path to the data directory
# PATH = os.path.join(r"D:\Sign-Language-Translator\greetings_data")

# # Create an array of action labels by listing the contents of the data directory
# actions = np.array(os.listdir(PATH))

# @app.route('/load_data')
# def load_data():
#     return jsonify({'actions': actions.tolist()})

# @app.route('/process_frame', methods=['POST'])
# def process_frame():
#     frame_data = request.json.get('frameData')  # Get frame data from the request
#     # Process the received frame data (perform image processing or any required action)
#     # Your processing logic here
    
#     # Return a response if needed
#     return 'Frame processed successfully'

# if __name__ == '__main__':
#     app.run(debug=True)

