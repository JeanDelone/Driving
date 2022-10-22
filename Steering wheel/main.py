import cv2 as cv
from time import time
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

scale_number = 1
cam0 = cv.VideoCapture(0)

with mp_hands.Hands(
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.3) as hands:
    while True:
        start = time()

        _, frame = cam0.read()
        if scale_number != 1:
            frame = cv.resize(frame, (int(frame.shape[1] // scale_number), int(frame.shape[0] // scale_number)))

        """ Processing of hand """
        results = hands.process(frame)
        if results.multi_hand_landmarks:
            for hand_lm in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_lm, mp_hands.HAND_CONNECTIONS)
        """ End of processing """


        # FPS Handling
        end = time()
        total_time = end - start
        if total_time != 0:
            fps = 1 / total_time
            print(f"FPS: {round(fps, 2)}")
            cv.putText(frame, f"FPS: {int(fps)}", (20,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2, 1)
        else:
            print(f"FPS: ???")
            cv.putText(frame, f"FPS: ???", (20,70), cv.FONT_HERSHEY_PLAIN, 2, (255,0,255), 2, 1)

        cv.imshow(f"1{cam0}", frame)

        if cv.waitKey(20) & 0xFF==ord("q"):
            break

cv.destroyAllWindows()