import cv2
import mediapipe as mp
import numpy as np
import os
import pickle

# Read gesture names from the file
with open('gestures.txt', 'r') as f:
    gestures = [line.strip() for line in f.readlines()]

# Initialize mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Other global variables
capture_mode = False
gesture_data = {gesture: [] for gesture in gestures}

# File paths
GESTURE_DATA_FILE = "gesture_data.pkl"

# Load stored gesture data if available
if os.path.exists(GESTURE_DATA_FILE):
    with open(GESTURE_DATA_FILE, 'rb') as f:
        gesture_data = pickle.load(f)
else:
    gesture_data = {gesture: [] for gesture in gestures}

# Save function to store gesture data
def save_gesture_data():
    with open(GESTURE_DATA_FILE, 'wb') as f:
        pickle.dump(gesture_data, f)

def capture_gesture(frame, gesture_name):
    # Process the frame and extract hand landmarks
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        # Convert landmarks to a flat list of coordinates
        landmarks_array = list(np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks]).flatten())
        gesture_data[gesture_name].append(landmarks_array)

def recognize_gesture(frame):
    # Process the frame and extract hand landmarks
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        landmarks = results.multi_hand_landmarks[0].landmark
        landmarks_array = list(np.array([[landmark.x, landmark.y, landmark.z] for landmark in landmarks]).flatten())

        min_distance = float('inf')
        recognized_gesture = None
        
        # Compare landmarks with stored gesture data
        for gesture_name, data in gesture_data.items():
            for example in data:
                distance = np.linalg.norm(np.array(example) - np.array(landmarks_array))
                if distance < min_distance:
                    min_distance = distance
                    recognized_gesture = gesture_name
        
        # Set a maximum threshold for gesture recognition
        max_distance = 0.5  # This value can be adjusted based on experimentation
        confidence = (1 - min_distance / max_distance) * 100
        return recognized_gesture, confidence
    else:
        return None, 0

def handle_action(gesture):
    if (gesture == 'Wave'):
        print("Waving")

# Mediapipe drawing utilities
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        continue

    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('k'):
        capture_mode = not capture_mode
    elif capture_mode and (ord('0') <= key <= ord('9')):
        index = key - ord('0')
        if 0 <= index < len(gestures):
            capture_gesture(frame, gestures[index])
            save_gesture_data()  # Save gesture data after capturing

    # Display recognized gesture on the screen
    if not capture_mode:
        gesture_name, confidence = recognize_gesture(frame)
        if gesture_name and confidence > 0:  # Only show if confidence is positive
            cv2.putText(frame, f"{gesture_name} ({confidence:.2f}%)", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            handle_action(gesture_name)
    else:
        cv2.putText(frame, "Capture Mode", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Draw keypoints and connections on hand
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Gesture Recognition", frame)

cap.release()
cv2.destroyAllWindows()
