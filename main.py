import cv2 as cv
import mediapipe as mp
import math
from constants import *
from audio_setup import *


def dist(first_point, second_point):
    return math.hypot(first_point[0]-second_point[0], first_point[1]-second_point[1])
def midpoint(first_point, second_point):
    mid_x = (first_point[0] + second_point[0]) // 2
    mid_y = (first_point[1] + second_point[1]) // 2
    return (mid_x, mid_y)


cam = cv.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
stream = sd.OutputStream(channels=1, callback=callback, samplerate=sample_rate, blocksize=4096)
stream.start()
while True:
    success, frame = cam.read()
    frame = cv.flip(frame, 1)
    frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    cv.imshow("Hand Detection", frame)
    left_found = False
    right_found = False
    pitch = 1
    volume = 1
    speed = 1
    if results.multi_hand_landmarks and results.multi_handedness:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            lp = []
            f_height, f_width, _ = frame.shape
            for index, landmark in enumerate(hand_landmarks.landmark):
                x_pixel = int(landmark.x * f_width)
                y_pixel = int(landmark.y * f_height)
                lp.append((x_pixel, y_pixel))
            mp_draw.draw_landmarks(frame, hand_landmarks,
                mp_hands.HAND_CONNECTIONS)
            label = hand_handedness.classification[0].label
            score = hand_handedness.classification[0].score

            if label == "Right":
                right_found = True
                index_tip_r = lp[HAND_LANDMARK_IDS["INDEX_FINGER_TIP"]]
                thumb_tip_r = lp[HAND_LANDMARK_IDS["THUMB_TIP"]]
                pitch = round(dist(index_tip_r, thumb_tip_r), 2)
                cv.line(frame, thumb_tip_r, index_tip_r, (255, 0, 0), thickness=2)
                cv.putText(frame, f"Pitch: {pitch}", midpoint(index_tip_r, thumb_tip_r),
                        cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            if label == "Left":
                left_found = True
                index_tip_l = lp[HAND_LANDMARK_IDS["INDEX_FINGER_TIP"]]
                thumb_tip_l = lp[HAND_LANDMARK_IDS["THUMB_TIP"]]
                volume = round(dist(index_tip_l, thumb_tip_l), 2)
                cv.line(frame, thumb_tip_l, index_tip_l, (255, 0, 0), thickness=2)
                cv.putText(frame, f"Volume: {volume}", midpoint(index_tip_l, thumb_tip_l),
                        cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            if left_found and right_found:
                speed = round(dist(midpoint(index_tip_l, thumb_tip_l), midpoint(index_tip_r, thumb_tip_r)), 2)
                cv.line(frame, midpoint(index_tip_l, thumb_tip_l), midpoint(index_tip_r, thumb_tip_r),
                        (255, 0, 0), thickness=2)
                speed_loc = list(midpoint(midpoint(index_tip_l, thumb_tip_l), midpoint(index_tip_r, thumb_tip_r)))
                speed_loc[0] = speed_loc[0] - 75
                speed_loc[1] = speed_loc[1] - 20
                cv.putText(frame, f"Speed: {speed}", speed_loc,
                            cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            change_pitch((pitch-200)/20)
            change_speed(speed/750)
            change_volume(volume/75)
        cv.imshow("Hand Detection", frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
stream.stop()
stream.close()
print("Stopped")