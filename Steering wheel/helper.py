from time import sleep
import cv2 as cv
import math
class Helper:

    
    def countdown(self, t):
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            sleep(1)
            t -= 1

    def __distance_between_2_points(self, p1, p2):
        return int(math.sqrt(((p2[0] - p1[0])**2) + ((p2[1] - p1[1])**2)))

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
            return hands_middle
    
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
            middle_of_hands = self.__hands_middle(hands)
            middle_of_steering_wheel = self.__steering_wheel_middle(middle_of_hands)
            wheel_radius = self.__steering_wheel_radius(middle_of_hands)

            # Drawing
            cv.circle(frame, middle_of_steering_wheel, wheel_radius, (128,128,128), 21)
            cv.line(frame, middle_of_hands[0], middle_of_hands[1], (128,128,128), 21)
            # cv.line(frame, middle_of_steering_wheel, )