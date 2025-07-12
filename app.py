import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
from gesture_utils import GestureRecognizer
import time
import re

# Configure Streamlit page
st.set_page_config(
    page_title="Hand Gesture Calculator",
    page_icon="🧮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'expression' not in st.session_state:
    st.session_state.expression = ""
if 'result' not in st.session_state:
    st.session_state.result = ""
if 'last_gesture' not in st.session_state:
    st.session_state.last_gesture = ""
if 'gesture_start_time' not in st.session_state:
    st.session_state.gesture_start_time = 0
if 'gesture_hold_duration' not in st.session_state:
    st.session_state.gesture_hold_duration = 1.5  # seconds

def safe_eval(expression):
    """Safely evaluate mathematical expressions"""
    try:
        # Remove any non-mathematical characters
        safe_expr = re.sub(r'[^0-9+\-*/().\s]', '', expression)
        
        # Check for empty expression
        if not safe_expr.strip():
            return "Error: Empty expression"
        
        # Evaluate the expression
        result = eval(safe_expr)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero"
    except Exception as e:
        return f"Error: Invalid expression"

def main():
    st.title("🧮 Hand Gesture Calculator")
    st.markdown("---")
    
    # Sidebar with instructions
    with st.sidebar:
        st.header("📋 Gesture Guide")
        st.markdown("""
        **Numbers (0-9):**
        - 0: Closed fist
        - 1-5: Show corresponding fingers
        - 6-9: Use both hands (5 + additional fingers)
        
        **Operators:**
        - ➕ Addition: Thumb + Index
        - ➖ Subtraction: Thumb + Pinky
        - ✖️ Multiplication: Index + Middle (V shape)
        - ➗ Division: Open palm
        - 🟰 Equals: Crossed index fingers
        - 🗑️ Clear: Two closed fists
        
        **Tips:**
        - Hold gesture for 1.5 seconds to register
        - Keep hand(s) visible in the camera
        - Good lighting improves accuracy
        """)
        
        # Settings
        st.header("⚙️ Settings")
        gesture_hold_duration = st.slider(
            "Gesture Hold Duration (seconds)", 
            0.5, 3.0, 1.5, 0.1
        )
        st.session_state.gesture_hold_duration = gesture_hold_duration
        
        confidence_threshold = st.slider(
            "Detection Confidence", 
            0.1, 1.0, 0.7, 0.05
        )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📹 Live Camera Feed")
        camera_placeholder = st.empty()
        
    with col2:
        st.header("🧮 Calculator")
        
        # Display current expression
        expression_container = st.container()
        with expression_container:
            st.subheader("Expression:")
            if st.session_state.expression:
                st.code(st.session_state.expression, language=None)
            else:
                st.code("Ready for input...", language=None)
        
        # Display result
        result_container = st.container()
        with result_container:
            st.subheader("Result:")
            if st.session_state.result:
                st.success(f"= {st.session_state.result}")
            else:
                st.info("Perform calculation to see result")
        
        # Current gesture display
        gesture_container = st.container()
        with gesture_container:
            st.subheader("Current Gesture:")
            if st.session_state.last_gesture:
                st.info(f"Detected: {st.session_state.last_gesture}")
            else:
                st.warning("No gesture detected")
        
        # Manual controls
        st.subheader("Manual Controls:")
        col_clear, col_eval = st.columns(2)
        with col_clear:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.expression = ""
                st.session_state.result = ""
        
        with col_eval:
            if st.button("🟰 Calculate", use_container_width=True):
                if st.session_state.expression:
                    st.session_state.result = safe_eval(st.session_state.expression)
    
    # Initialize gesture recognizer
    gesture_recognizer = GestureRecognizer(confidence_threshold)
    
    # Camera capture
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        st.error("❌ Could not access camera. Please check your camera permissions.")
        return
    
    # Main processing loop
    stframe = camera_placeholder.empty()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                st.error("❌ Failed to capture frame from camera")
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Process gesture
            processed_frame, gesture = gesture_recognizer.process_frame(frame)
            
            # Handle gesture recognition with hold duration
            current_time = time.time()
            
            if gesture and gesture != "unknown":
                if gesture == st.session_state.last_gesture:
                    # Same gesture, check if held long enough
                    if current_time - st.session_state.gesture_start_time >= st.session_state.gesture_hold_duration:
                        # Process the gesture
                        process_gesture(gesture)
                        st.session_state.gesture_start_time = current_time  # Reset timer
                else:
                    # New gesture detected
                    st.session_state.last_gesture = gesture
                    st.session_state.gesture_start_time = current_time
            else:
                # No gesture or unknown gesture
                if current_time - st.session_state.gesture_start_time > 2.0:  # Reset after 2 seconds
                    st.session_state.last_gesture = ""
            
            # Convert BGR to RGB for Streamlit
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            
            # Display frame
            stframe.image(frame_rgb, channels="RGB", use_column_width=True)
            
            # Small delay to prevent excessive processing
            time.sleep(0.1)
            
    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
    
    finally:
        cap.release()

def process_gesture(gesture):
    """Process recognized gesture and update calculator state"""
    
    # Numbers 0-9
    if gesture.isdigit():
        st.session_state.expression += gesture
    
    # Operators
    elif gesture == "add":
        if st.session_state.expression and not st.session_state.expression.endswith(('+', '-', '*', '/')):
            st.session_state.expression += " + "
    
    elif gesture == "subtract":
        if st.session_state.expression and not st.session_state.expression.endswith(('+', '-', '*', '/')):
            st.session_state.expression += " - "
    
    elif gesture == "multiply":
        if st.session_state.expression and not st.session_state.expression.endswith(('+', '-', '*', '/')):
            st.session_state.expression += " * "
    
    elif gesture == "divide":
        if st.session_state.expression and not st.session_state.expression.endswith(('+', '-', '*', '/')):
            st.session_state.expression += " / "
    
    # Special commands
    elif gesture == "equals":
        if st.session_state.expression:
            st.session_state.result = safe_eval(st.session_state.expression)
    
    elif gesture == "clear":
        st.session_state.expression = ""
        st.session_state.result = ""

if __name__ == "__main__":
    main()
