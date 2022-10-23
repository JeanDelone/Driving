from time import sleep
import cv2 as cv
import math
from keys import PressKey, ReleaseKey, W,S,A,D
import vgamepad as vg



class Helper:

    def __init__(self):
        self.middle_of_hands = [[],[]]
        self.steering_number = 50
        self.max_steering_number = 240
        self.primary_wheel_color = (30,30,30)
        self.secondary_wheel_color = (72,72,72)
        self.WHITE = (255,255,255)
        self.PINK = (255,0,255)
        self.gamepad = vg.VX360Gamepad()
    
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
            y1y2 = y1 - y2
            if (y1y2) >= self.steering_number:
                if y1y2 >= self.max_steering_number:
                    steer_value = 32767
                    if x1 - x2 > 0:
                        print("steering left")
                        self.gamepad.reset()
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("steering right")
                        self.gamepad.reset()
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
                # print(f"a: {steer_value}")
                else:
                    steer_value = int(32676 * ((y1y2)/self.max_steering_number))
                    if x1 - x2 > 0:
                        print("steering left")
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value=111)  # value between 0 and 255
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("steering right")
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value=111)  # value between 0 and 255
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
            elif (y1y2) <= - self.steering_number:
                if y1y2 >= self.max_steering_number:
                    steer_value = 32767
                    if x1 - x2 > 0:
                        print("steering left")
                        self.gamepad.reset()
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("steering right")
                        self.gamepad.reset()
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
                # print(f"a: {steer_value}")
                else:
                    steer_value = int(32676 * ((y1y2)/self.max_steering_number))
                    if x1 - x2 > 0:
                        print("steering left")
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value=111)  # value between 0 and 255
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("steering right")
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value=111)  # value between 0 and 255
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
            else:
                self.gamepad.reset()
                self.gamepad.right_trigger(value=255)  # value between 0 and 255
                self.gamepad.update()
                print("going forward")
        else:
            # ReleaseKey(W)
            # ReleaseKey(A)
            # ReleaseKey(D)
            # PressKey(S)
            print("backing")


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

    def __third_point_on_circle(self, hands, midpoint, lower = True):
        points_relative = [[hands[0][0] - midpoint[0], hands[0][1] - midpoint[1]], [hands[1][0] - midpoint[0], hands[1][1] - midpoint[1]]]

        midpoint_points_relative = [[points_relative[0][1], - points_relative[0][0]], [points_relative[1][1], - points_relative[1][0]]]
        midpoint_points = [[midpoint_points_relative[0][0] + midpoint[0], midpoint_points_relative[0][1] + midpoint[1]], [midpoint_points_relative[1][0] + midpoint[0], midpoint_points_relative[1][1] + midpoint[1]]]
        if midpoint_points[0][1] >= midpoint_points[1][1]:
            if lower:
                return midpoint_points[0]
            return midpoint_points[1]
        else:
            if lower:
                return midpoint_points[1]
            return midpoint_points[0]
    
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
                cv.circle(frame, middle_of_steering_wheel, wheel_radius, self.secondary_wheel_color, 21)
                cv.line(frame, self.middle_of_hands[0], self.middle_of_hands[1], self.secondary_wheel_color, 21)
                cv.line(frame, middle_of_steering_wheel, third_point, self.secondary_wheel_color, 21)
                cv.line(frame, middle_of_steering_wheel, third_point, self.primary_wheel_color, 16)
                cv.circle(frame, middle_of_steering_wheel, wheel_radius, self.primary_wheel_color, 16)
                cv.line(frame, self.middle_of_hands[0], self.middle_of_hands[1], self.primary_wheel_color, 16)



                # drawing car logo
                cv.circle(frame, middle_of_steering_wheel, 50, self.primary_wheel_color, -1)
                cv.circle(frame, middle_of_steering_wheel, 43, self.secondary_wheel_color, 2)
                # cv.line(frame, middle_of_steering_wheel, )
            except:
                print("CIRCLE DRAWING ERROR")