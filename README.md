# GestureStage

GestureStage is a real-time audiovisual effects application controlled by hand gestures. Using computer vision and machine learning, the system tracks hand movements through a webcam and maps recognized gestures to visual and audio effects.

## Project Goals

* Real-time hand tracking using MediaPipe
* Custom gesture recognition from landmark positions
* Visual effects controlled by hand gestures
* Audio effects controlled by hand gestures
* Smooth, low-latency interaction
* Portfolio-quality machine learning project

## Tech Stack

* Python
* OpenCV
* MediaPipe Tasks API
* NumPy

## Project Structure

```text
gesture-stage/
├── app/
│   ├── webcam_test.py
│   └── hand_tracker.py
├── models/
│   └── hand_landmarker.task
├── assets/
├── docs/
├── requirements.txt
└── README.md
```

## Progress

### Week 1 — Hand Tracking ✅

Completed:

* Python virtual environment setup
* OpenCV webcam pipeline
* MediaPipe Hand Landmarker integration
* Real-time hand landmark detection
* Landmark coordinate extraction
* Landmark visualization on webcam feed
* Landmark index visualization (0–20)
* GitHub repository setup and version control

Current result:

* Hand landmarks are tracked in real time
* Landmark coordinates can be accessed programmatically
* Landmark indices are displayed directly on the video feed

### Week 2 — Gesture Recognition (In Progress)

Planned:

* Learn MediaPipe landmark anatomy
* Detect individual finger states (up/down)
* Build custom gesture classifiers
* Recognize gestures such as:

  * Open Hand
  * Fist
  * Peace Sign
  * Thumbs Up

## Future Roadmap

* Gesture-controlled visual effects
* Gesture-controlled audio effects
* Performance optimization
* Demo video and portfolio presentation

## Author

Roman Stikhin
