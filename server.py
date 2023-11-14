from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

GESTURE_ACTION_FILE = "gesture_action_mappings.pkl"

# Load or initialize gesture-action mappings
if os.path.exists(GESTURE_ACTION_FILE):
    with open(GESTURE_ACTION_FILE, 'rb') as f:
        gesture_action_mappings = pickle.load(f)
else:
    gesture_action_mappings = {}

@app.route('/map-gesture', methods=['POST'])
def map_gesture():
    data = request.json
    gesture_name = data.get('gesture')
    action = data.get('action')
    gesture_action_mappings[gesture_name] = action

    with open(GESTURE_ACTION_FILE, 'wb') as f:
        pickle.dump(gesture_action_mappings, f)

    return jsonify({'message': 'Gesture mapping saved successfully'})

@app.route('/gestures', methods=['GET'])
def get_gestures():
    with open('gestures.txt', 'r') as f:
        gestures = [line.strip() for line in f.readlines()]
    return jsonify(gestures)

if __name__ == '__main__':
    app.run(debug=True)
