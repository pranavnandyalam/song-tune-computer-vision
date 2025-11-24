import sounddevice as sd
import numpy as np
import threading
import time
from pedalboard.io import AudioFile
from pedalboard import Pedalboard, PitchShift
from scipy import signal

with AudioFile('your_audio_file.ext') as f:
    audio = f.read(f.frames)
    sample_rate = f.samplerate

audio_mono = audio.mean(axis=0) if audio.shape[0] == 2 else audio[0]
params = {'speed': 1.0, 'pitch': 0, 'volume': 1.0}
position = 0
board = Pedalboard([PitchShift(semitones=0)])

def callback(outdata, frames, time_info, status):
    global position
    needed_src = int(frames * params['speed'])
    if position + needed_src >= len(audio_mono):
        position = 0
    chunk = audio_mono[position:position + needed_src]
    position += needed_src
    resampled = signal.resample(chunk, frames)
    board[0].semitones = params['pitch']
    pitched = board(resampled.reshape(1, -1), sample_rate)[0]
    out = np.clip(pitched * params['volume'], -1.0, 1.0)
    outdata[:, 0] = out

def change_speed(speed):
    params['speed'] = np.clip(speed, 0.1, 4.0)
def change_pitch(semitones):
    params['pitch'] = np.clip(semitones, -12, 12)
def change_volume(volume):
    params['volume'] = np.clip(volume, 0.0, 4.0)
