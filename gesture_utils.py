import cv2
import mediapipe as mp
import numpy as np
import math

class GestureRecognizer:
    def __init__(self, confidence_threshold=0.7):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=confidence_threshold,
            min_tracking_confidence=confidence_threshold
        )
        self.mp_drawing = mp.solutions.drawing_utils
        self.confidence_threshold = confidence_threshold
        
    def process_frame(self, frame):
        """Process frame and return annotated frame with detected gesture"""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        
        # Draw hand landmarks
        annotated_frame = frame.copy()
        gesture = "unknown"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    annotated_frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                )
            
            # Recognize gesture
            gesture = self.recognize_gesture(results.multi_hand_landmarks)
        
        # Display gesture on frame
        cv2.putText(
            annotated_frame, 
            f"Gesture: {gesture}", 
            (10, 30), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            1, 
            (0, 255, 0), 
            2
        )
        
        return annotated_frame, gesture
    
    def recognize_gesture(self, hand_landmarks_list):
        """Recognize gesture from hand landmarks"""
        if not hand_landmarks_list:
            return "unknown"
        
        # Single hand gestures
        if len(hand_landmarks_list) == 1:
            return self.recognize_single_hand_gesture(hand_landmarks_list[0])
        
        # Two hand gestures
        elif len(hand_landmarks_list) == 2:
            return self.recognize_two_hand_gesture(hand_landmarks_list)
        
        return "unknown"
    
    def recognize_single_hand_gesture(self, hand_landmarks):
        """Recognize gestures from a single hand"""
        landmarks = hand_landmarks.landmark
        
        # Get finger states (extended or not)
        fingers = self.get_finger_states(landmarks)
        extended_count = sum(fingers)
        
        # Number recognition (0-5)
        if extended_count == 0:
            return "0"  # Closed fist
        elif extended_count == 1:
            return "1"
        elif extended_count == 2:
            # Check for specific two-finger gestures
            if fingers[1] and fingers[2]:  # Index and middle
                if self.is_v_shape(landmarks):
                    return "multiply"  # V shape for multiplication
                else:
                    return "2"
            elif fingers[0] and fingers[1]:  # Thumb and index
                return "add"  # Addition gesture
            elif fingers[0] and fingers[4]:  # Thumb and pinky
                return "subtract"  # Subtraction gesture
            else:
                return "2"
        elif extended_count == 3:
            return "3"
        elif extended_count == 4:
            return "4"
        elif extended_count == 5:
            # Check if it's an open palm (division) or just number 5
            if self.is_open_palm(landmarks):
                return "divide"
            else:
                return "5"
        
        return "unknown"
    
    def recognize_two_hand_gesture(self, hand_landmarks_list):
        """Recognize gestures from two hands"""
        hand1_landmarks = hand_landmarks_list[0].landmark
        hand2_landmarks = hand_landmarks_list[1].landmark
        
        # Get finger states for both hands
        fingers1 = self.get_finger_states(hand1_landmarks)
        fingers2 = self.get_finger_states(hand2_landmarks)
        
        extended1 = sum(fingers1)
        extended2 = sum(fingers2)
        
        # Two closed fists = Clear
        if extended1 == 0 and extended2 == 0:
            return "clear"
        
        # Crossed index fingers = Equals
        if (fingers1[1] and sum(fingers1) == 1 and 
            fingers2[1] and sum(fingers2) == 1):
            if self.are_fingers_crossed(hand1_landmarks, hand2_landmarks):
                return "equals"
        
        # Number combinations (6-9)
        total_extended = extended1 + extended2
        if 6 <= total_extended <= 9:
            return str(total_extended)
        
        return "unknown"
    
    def get_finger_states(self, landmarks):
        """Determine which fingers are extended"""
        fingers = []
        
        # Thumb (compare x coordinates due to thumb orientation)
        if landmarks[4].x > landmarks[3].x:  # Right hand
            fingers.append(landmarks[4].x > landmarks[3].x)
        else:  # Left hand
            fingers.append(landmarks[4].x < landmarks[3].x)
        
        # Other fingers (compare y coordinates)
        finger_tips = [8, 12, 16, 20]  # Index, middle, ring, pinky
        finger_pips = [6, 10, 14, 18]
        
        for tip, pip in zip(finger_tips, finger_pips):
            fingers.append(landmarks[tip].y < landmarks[pip].y)
        
        return fingers
    
    def is_v_shape(self, landmarks):
        """Check if index and middle fingers form a V shape"""
        # Get positions of finger tips and base
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        base = landmarks[9]  # Base between index and middle
        
        # Calculate angle between the two fingers
        v1 = np.array([index_tip.x - base.x, index_tip.y - base.y])
        v2 = np.array([middle_tip.x - base.x, middle_tip.y - base.y])
        
        # Calculate angle
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
        angle_degrees = np.degrees(angle)
        
        # V shape typically has angle between 30-90 degrees
        return 30 <= angle_degrees <= 90
    
    def is_open_palm(self, landmarks):
        """Check if hand is in open palm position"""
        # All fingers should be extended and spread
        fingers = self.get_finger_states(landmarks)
        
        if sum(fingers) != 5:
            return False
        
        # Check if fingers are spread (measure distances between finger tips)
        finger_tips = [4, 8, 12, 16, 20]  # Thumb, index, middle, ring, pinky
        
        distances = []
        for i in range(len(finger_tips) - 1):
            tip1 = landmarks[finger_tips[i]]
            tip2 = landmarks[finger_tips[i + 1]]
            distance = math.sqrt((tip1.x - tip2.x)**2 + (tip1.y - tip2.y)**2)
            distances.append(distance)
        
        # If fingers are spread, average distance should be above threshold
        avg_distance = sum(distances) / len(distances)
        return avg_distance > 0.08  # Threshold for spread fingers
    
    def are_fingers_crossed(self, hand1_landmarks, hand2_landmarks):
        """Check if index fingers from both hands are crossed"""
        # Get index finger tips
        index1 = hand1_landmarks[8]
        index2 = hand2_landmarks[8]
        
        # Get hand centers (approximate)
        center1 = hand1_landmarks[9]  # Base of middle finger
        center2 = hand2_landmarks[9]
        
        # Check if fingers are close to each other and crossing
        distance = math.sqrt((index1.x - index2.x)**2 + (index1.y - index2.y)**2)
        
        # Also check if hands are positioned to allow crossing
        hand_distance = math.sqrt((center1.x - center2.x)**2 + (center1.y - center2.y)**2)
        
        return distance < 0.05 and hand_distance < 0.3
