Hand-Controlled Audio Player
============================

Use Mediapipe hand tracking and OpenCV to control audio playback: right hand pinching adjusts pitch, left hand pinching adjusts volume, and the distance between both hands controls playback speed.

Prerequisites
-------------
- Python 3.9+ and pip
- A webcam and working speakers/headphones
- PortAudio available for `sounddevice` (on macOS: `brew install portaudio` if you hit device errors)

Setup
-----
1) Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate
```
2) Install dependencies:
```
pip install --upgrade pip
pip install opencv-python mediapipe sounddevice pedalboard scipy numpy
```
3) Supply an audio file:
- Place a short audio file in the repo and update `audio_setup.py` to point to it (replace `your_audio_file.ext` with the actual filename, e.g., `audios/loop.wav`).

Run
---
```
python main.py
```
- Allow camera/microphone permissions when prompted by your OS.
- Press `q` to quit the window.

Controls
--------
- Right hand: distance between thumb tip and index tip => pitch.
- Left hand: distance between thumb tip and index tip => volume.
- Both hands together: distance between the two pinches => playback speed.

Notes
-----
- Keep `venv/` and large media out of git; they are already in `.gitignore`.
- If audio stutters, try a smaller `blocksize` in `audio_setup.py` or a lower camera resolution in `main.py`.
