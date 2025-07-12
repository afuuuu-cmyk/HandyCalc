# HandyCalc – Hand Gesture Based Calculator

HandyCalc is a real-time hand gesture–controlled calculator built with Python, OpenCV, MediaPipe, and Streamlit.

## Features
- Real-time webcam input
- Recognizes numbers (0–5) and operations (+, -, *, =)
- Use gestures to enter math expressions
- Streamlit UI to visualize live camera and results

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Controls
- 0 fingers: Clear
- 1-5 fingers: Digits 1-5
- 2 fingers: +
- 3 fingers: -
- 4 fingers: *
- 5 fingers: Evaluate (=)
