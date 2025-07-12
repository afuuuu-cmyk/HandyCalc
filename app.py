import streamlit as st
import cv2
import mediapipe as mp
import numpy as np

st.set_page_config(page_title="HandyCalc - Hand Gesture Calculator")

st.title("🤖 HandyCalc: Hand Gesture Calculator")
st.write("Show your fingers to the webcam to calculate using gestures!")

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
result = ""
frame_placeholder = st.empty()
output_placeholder = st.empty()

def count_fingers(hand_landmarks):
    finger_tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_landmarks.landmark[finger_tips_ids[0]].x < hand_landmarks.landmark[finger_tips_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # 4 Fingers
    for id in range(1, 5):
        if hand_landmarks.landmark[finger_tips_ids[id]].y < hand_landmarks.landmark[finger_tips_ids[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

def map_gesture_to_input(count):
    mapping = {
        0: '0',
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5'
    }
    return mapping.get(count, '')

st.write("Use 1–5 fingers to input digits. Fist (0) to clear, 2 fingers for '+', 3 for '-', 4 for '*', 5 for '='")

while True:
    ret, frame = cap.read()
    if not ret:
        st.error("Failed to access webcam.")
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result_hands = hands.process(rgb_frame)

    if result_hands.multi_hand_landmarks:
        for handLms in result_hands.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            count = count_fingers(handLms)

            if count == 0:
                result = ""
            elif count == 2:
                result += '+'
            elif count == 3:
                result += '-'
            elif count == 4:
                result += '*'
            elif count == 5:
                try:
                    evaluated = eval(result)
                    result = str(evaluated)
                except:
                    result = "Error"
            else:
                result += map_gesture_to_input(count)

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_placeholder.image(frame, channels="RGB")
    output_placeholder.subheader(f"🧮 Result: `{result}`")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
