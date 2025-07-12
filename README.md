# 🧮 Hand Gesture Calculator

A real-time hand gesture-based calculator built with Python, OpenCV, MediaPipe, and Streamlit. Perform mathematical calculations using intuitive hand gestures captured through your webcam!

## ✨ Features

### 🔢 Number Recognition (0-9)
- **0**: Closed fist
- **1-5**: Show corresponding number of fingers
- **6-9**: Use both hands (5 fingers + additional fingers from other hand)

### 🔣 Operator Recognition
- **➕ Addition**: Thumb + Index finger
- **➖ Subtraction**: Thumb + Pinky finger
- **✖️ Multiplication**: Index + Middle fingers in V shape
- **➗ Division**: Open palm (all fingers spread)
- **🟰 Equals**: Crossed index fingers from both hands
- **🗑️ Clear**: Two closed fists

### 🖥️ User Interface
- Real-time webcam feed with gesture overlay
- Live expression building
- Instant calculation results
- Manual controls as backup
- Adjustable gesture sensitivity
- Comprehensive gesture guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Webcam access
- Good lighting conditions

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

3. **Run the application**:
   \`\`\`bash
   streamlit run app.py
   \`\`\`

4. **Open your browser** and navigate to the provided local URL (usually \`http://localhost:8501\`)

## 📱 Usage Guide

### Getting Started
1. **Allow camera access** when prompted by your browser
2. **Position yourself** so your hands are clearly visible in the camera
3. **Hold gestures** for 1.5 seconds (adjustable) to register them
4. **Build expressions** by showing numbers and operators in sequence
5. **Calculate results** using the equals gesture or manual button

### Tips for Best Results
- 🔆 **Good lighting**: Ensure your hands are well-lit
- 📏 **Proper distance**: Keep hands 1-2 feet from the camera
- 🤚 **Clear gestures**: Make distinct, deliberate hand shapes
- ⏱️ **Hold steady**: Maintain gestures for the required duration
- 🧹 **Clean background**: Avoid cluttered backgrounds behind your hands

### Example Calculation
1. Show **2 fingers** → "2" appears in expression
2. Show **thumb + index** → " + " is added
3. Show **3 fingers** → "3" is added
4. **Cross index fingers** → Result "5" is calculated

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web interface
- **Computer Vision**: OpenCV for camera handling
- **Hand Detection**: MediaPipe for robust hand landmark detection
- **Gesture Recognition**: Custom algorithm analyzing finger positions and hand shapes

### Key Components
- \`app.py\`: Main Streamlit application with UI and camera handling
- \`gesture_utils.py\`: Core gesture recognition logic and hand analysis
- \`requirements.txt\`: Python dependencies
- \`README.md\`: Documentation and setup guide

### Gesture Recognition Algorithm
1. **Hand Detection**: MediaPipe identifies hand landmarks
2. **Finger Analysis**: Determines which fingers are extended
3. **Shape Recognition**: Analyzes hand shapes for operators
4. **Multi-hand Processing**: Handles two-hand gestures for numbers 6-9 and special commands
5. **Temporal Filtering**: Requires gesture hold duration to prevent false positives

## 🌐 Deployment

### Streamlit Cloud Deployment
1. **Push code to GitHub repository**
2. **Connect to Streamlit Cloud** at [share.streamlit.io](https://share.streamlit.io)
3. **Deploy directly** from your GitHub repository
4. **Share your app** with the generated URL

### Local Network Deployment
\`\`\`bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8501
\`\`\`

## ⚙️ Configuration

### Adjustable Settings
- **Gesture Hold Duration**: Time required to register a gesture (0.5-3.0 seconds)
- **Detection Confidence**: MediaPipe confidence threshold (0.1-1.0)
- **Camera Resolution**: Modify in \`cv2.VideoCapture()\` settings

### Customization Options
- **Add new gestures**: Extend \`gesture_utils.py\` with custom recognition logic
- **Modify UI**: Customize Streamlit interface in \`app.py\`
- **Change gesture mappings**: Update gesture-to-action mappings

## 🔧 Troubleshooting

### Common Issues

**Camera not working**:
- Check camera permissions in browser
- Ensure no other applications are using the camera
- Try different camera indices: \`cv2.VideoCapture(1)\` or \`cv2.VideoCapture(2)\`

**Poor gesture recognition**:
- Improve lighting conditions
- Adjust detection confidence in settings
- Ensure hands are clearly visible and unobstructed
- Check camera focus and resolution

**Performance issues**:
- Close other resource-intensive applications
- Reduce camera resolution if needed
- Adjust frame processing rate

### Error Messages
- **"Could not access camera"**: Check camera permissions and availability
- **"Invalid expression"**: Ensure proper operator placement in expressions
- **"Division by zero"**: Avoid dividing by zero in calculations

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional gesture recognition patterns
- Enhanced UI/UX design
- Performance optimizations
- Mobile device compatibility
- Advanced mathematical operations

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **MediaPipe**: Google's framework for hand detection
- **OpenCV**: Computer vision library
- **Streamlit**: Web app framework
- **NumPy**: Numerical computing library

---

**Happy calculating with gestures! 🧮✋**
