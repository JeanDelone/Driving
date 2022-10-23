from time import sleep
import cv2 as cv
import math
from keys import PressKey, ReleaseKey, W,S,A,D

class Helper:

    def __init__(self):
        self.middle_of_hands = [[],[]]
        self.steering_number = 100
    
    def countdown(self, t):
        print("\n")
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            sleep(1)
            t -= 1

    def __distance_between_2_points(self, p1, p2):
        return int(math.sqrt(((p2[0] - p1[0])**2) + ((p2[1] - p1[1])**2)))

    def __average(self, points):
        if len(points[0]) != 0 and len(points[1]) != 0:
            y1 = points[0][1]
            y2 = points[1][1]
            print(f" y1 = {y1}, y2 = {y2}")
            return int(math.sqrt(((y1 + y2) // 2)**2))

    def steering(self):
        if len(self.middle_of_hands[0]) != 0 and len(self.middle_of_hands[1]) != 0:
            y1 = self.middle_of_hands[0][1]
            y2 = self.middle_of_hands[1][1]
            x1 = self.middle_of_hands[0][0]
            x2 = self.middle_of_hands[1][0]
            if (y1 - y2) >= self.steering_number:
                if x1 - x2 > 0:
                # ReleaseKey(W)
                # ReleaseKey(D)
                # PressKey(A)
                    print("steering left")
                    ReleaseKey(S)
                    ReleaseKey(W)
                    ReleaseKey(D)
                    PressKey(A)
                else:
                    print("steering right")
                    ReleaseKey(S)
                    ReleaseKey(W)
                    ReleaseKey(A)
                    PressKey(D)
            elif int(y1 - y2) <= - self.steering_number:
                if x1 - x2 < 0:
                    print("steering left")
                    ReleaseKey(S)
                    ReleaseKey(W)
                    ReleaseKey(D)
                    PressKey(A)
                else:
                    print("steering right")
                    ReleaseKey(S)
                    ReleaseKey(W)
                    ReleaseKey(A)
                    PressKey(D)
            else:
                ReleaseKey(S)
                ReleaseKey(A)
                ReleaseKey(D)
                PressKey(W)
                print("going forward")
        else:
            ReleaseKey(W)
            ReleaseKey(A)
            ReleaseKey(D)
            PressKey(S)
            print("backing")
            # print(y_distance)
            # if y_distance <= 100:
            #     PressKey(W)
            #     print("going forward")
            # elif y_distance > 100:
            #     if hands[0][1] >= hands[1][1]:
            #         PressKey(A)
            #         print("steering left")
            #     else:
            #         print("steering right")
            #         PressKey(D)


    def __midpoint(self, p1, p2):
        return (int(((p1[0] + p2[0]) / 2)), int(((p1[1] + p2[1]) / 2)))

    def __hands_middle(self, hands = []):
        if len(hands[0]) != 0 and len(hands[1]) != 0:
            sumx = 0
            sumy = 0
            hands_middle = [[],[]]
            for id, hand in enumerate(hands):
                for points in hand:
                    sumx += points[0]    
                    sumy += points[1]
                hands_middle[id].append(int(sumx / len(hands[id])))
                hands_middle[id].append(int(sumy / len(hands[id])))
                sumx = 0
                sumy = 0
            self.middle_of_hands = hands_middle

    def __third_point_on_circle(self, hands, midpoint):
        points_relative = [[hands[0][0] - midpoint[0], hands[0][1] - midpoint[1]], [hands[1][0] - midpoint[0], hands[1][1] - midpoint[1]]]

        midpoint_points_relative = [[points_relative[0][1], - points_relative[0][0]], [points_relative[1][1], - points_relative[1][0]]]
        midpoint_points = [[midpoint_points_relative[0][0] + midpoint[0], midpoint_points_relative[0][1] + midpoint[1]], [midpoint_points_relative[1][0] + midpoint[0], midpoint_points_relative[1][1] + midpoint[1]]]
        if midpoint_points[0][1] >= midpoint_points[1][1]:
            return midpoint_points[0]
        else:
            return midpoint_points[1]
    
    def __steering_wheel_radius(self, hands):
        if hands != None:
            if len(hands[0]) and len(hands[1]) != 0:
                return self.__distance_between_2_points(hands[0], hands[1]) // 2
    
    def __steering_wheel_middle(self, hands):
        if hands != None:
            if len(hands[0]) != 0 and len(hands[1]) != 0:
                return self.__midpoint(hands[0], hands[1])

    def draw_steering_wheel(self, frame, hands):
        if len(hands[0]) != 0 and len(hands[1]) != 0:
            try:
                self.__hands_middle(hands)
                middle_of_steering_wheel = self.__steering_wheel_middle(self.middle_of_hands)
                wheel_radius = self.__steering_wheel_radius(self.middle_of_hands)
                third_point = self.__third_point_on_circle(self.middle_of_hands, middle_of_steering_wheel)
                
                # Drawing outside circle and middle line
                cv.circle(frame, middle_of_steering_wheel, wheel_radius, (192,192,192), 21)
                cv.line(frame, self.middle_of_hands[0], self.middle_of_hands[1], (192,192,192), 21)
                cv.line(frame, middle_of_steering_wheel, third_point, (192,192,192), 21)
                cv.line(frame, middle_of_steering_wheel, third_point, (0,0,0), 16)
                cv.circle(frame, middle_of_steering_wheel, wheel_radius, (0,0,0), 16)
                cv.line(frame, self.middle_of_hands[0], self.middle_of_hands[1], (0,0,0), 16)

                # Drawing half-line from middle to bottom


                # drawing car logo
                cv.circle(frame, middle_of_steering_wheel, 50, (0,0,0), -1)
                cv.circle(frame, middle_of_steering_wheel, 43, (192,192,192), 2)
            except:
                print("CIRCLE DRAWING ERROR")