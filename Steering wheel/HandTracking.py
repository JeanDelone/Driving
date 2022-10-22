"""
This is a template for hand-tracking in future projects
"""

import mediapipe as mp
import cv2 as cv
from time import time

class HandDetector:
    def __init__(self, cam, mode = False, maxHands = 2, detectionCon = 0.5, trackCon = 0.35,):
        self.cam = cam
        _, self.frame = cam.read()
        self.height = self.frame.shape[0]
        self.width = self.frame.shape[1]
        
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.result = None
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(min_detection_confidence = self.detectionCon, min_tracking_confidence = self.trackCon)
        self.mp_drawing = mp.solutions.drawing_utils

    def process_hands(self, frame, draw = False):
        imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        if draw:
            if self.result.multi_hand_landmarks:
                for hand_lm in self.result.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_lm, self.mp_hands.HAND_CONNECTIONS)
        return frame

    def find_positions(self, positions = []):
        lm_list_1 = []
        lm_list_2 = []
        combined_list = [lm_list_1, lm_list_2]
        if self.result.multi_hand_landmarks:
            for hand_id, hand in enumerate(self.result.multi_hand_landmarks):
                for id, lm in enumerate(hand.landmark):
                    try:
                        if id in positions and hand_id <= 1:
                            combined_list[hand_id].append([int(lm.x * self.width), int(lm.y * self.height)])
                    except:
                        pass
        return combined_list

if __name__ == "__main__":
    cam0 = cv.VideoCapture(0)

    hand_detector = HandDetector(cam0)

    while True:
        start = time()
        _, frame = cam0.read()
        
        frame = hand_detector.process_hands(frame)
        print(hand_detector.find_positions())
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

        cv.imshow(f"{cam0}", frame)
        if cv.waitKey(20) & 0xFF==ord("q"):
            break

    cam0.release()
    cv.destroyAllWindows()