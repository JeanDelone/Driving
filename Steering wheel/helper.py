from time import sleep
import cv2 as cv
import math
from keys import PressKey, ReleaseKey, W,S,A,D
import vgamepad as vg



class Helper:

    """ Min and max steering values are thresholds, where 
    difference between y values of hands determine how much you
    are steering on joystick. If this difference is below min_steering_number, you
    don't steer at all, when it's at least max_steering_number, you steer
    maximum amount"""
    def __init__(self):
        self.middle_of_hands = [[],[]]
        self.min_steering_number = 50
        self.max_steering_number = 220
        self.primary_wheel_color = (30,30,30)
        self.secondary_wheel_color = (72,72,72)
        self.low_turn_value = 171
        self.high_turn_value = 69
        self.WHITE = (255,255,255)
        self.PINK = (255,0,255)
        self.gamepad = vg.VX360Gamepad()
    
    def countdown(self, t):
        # print("\n")
        while t:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print(timer, end="\r")
            sleep(1)
            t -= 1

    def __distance_between_2_points(self, p1, p2):
        return int(math.sqrt(((p2[0] - p1[0])**2) + ((p2[1] - p1[1])**2)))

    """ Based on camera input, this function determines what steering inputs
    should be sent. It uses xbox controller from vgamepad library.
    x1 - x2 is used to determine which hand is which"""
    def steering(self):
        # If both hands are detected on cam, process further, if not: reverse
        if len(self.middle_of_hands[0]) != 0 and len(self.middle_of_hands[1]) != 0:
            y1 = self.middle_of_hands[0][1]
            y2 = self.middle_of_hands[1][1]
            x1 = self.middle_of_hands[0][0]
            x2 = self.middle_of_hands[1][0]
            hands_y_difference = y1 - y2

            if x1 - x2 > 0:
                if (hands_y_difference) >= self.min_steering_number:
                    if hands_y_difference >= self.max_steering_number:
                        print("1 hard left")
                        steer_value = 32767
                        self.gamepad.reset()
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("2 low left")
                        steer_value = int(32676 * ((hands_y_difference)/self.max_steering_number))
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value = self.low_turn_value)  # value between 0 and 255
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                elif (hands_y_difference) <= - self.min_steering_number:
                    if hands_y_difference <= - self.max_steering_number:
                        print("3 hard right")
                        steer_value = 32767
                        self.gamepad.reset()
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("4 low right")
                        steer_value = int(32676 * ((hands_y_difference)/self.max_steering_number))
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value = self.low_turn_value)  # value between 0 and 255
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                else:
                    print("forward")
                    self.gamepad.reset()
                    self.gamepad.right_trigger(value=255)
                    self.gamepad.update()
                    
            else:
                if (hands_y_difference) >= self.min_steering_number:
                    if hands_y_difference >= self.max_steering_number:
                        print("5 hard right")
                        steer_value = 32767
                        self.gamepad.reset()
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("6 low right")
                        steer_value = int(32676 * ((hands_y_difference)/self.max_steering_number))
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value = self.low_turn_value)  # value between 0 and 255
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
                elif (hands_y_difference) <= - self.min_steering_number:
                    if hands_y_difference <= - self.max_steering_number:
                        print("7 hard left")
                        steer_value = 32767
                        self.gamepad.reset()
                        self.gamepad.left_joystick(-steer_value, 0)
                        self.gamepad.update()
                    else:
                        print("8 low left")
                        steer_value = int(32676 * ((hands_y_difference)/self.max_steering_number))
                        self.gamepad.reset()
                        self.gamepad.right_trigger(value = self.low_turn_value)  # value between 0 and 255
                        self.gamepad.left_joystick(steer_value, 0)
                        self.gamepad.update()
                else:
                    print("forward")
                    self.gamepad.reset()
                    self.gamepad.right_trigger(value=255)
                    self.gamepad.update()
        else:
            print("backing")
            self.gamepad.reset()
            self.gamepad.left_trigger(value=150)
            self.gamepad.update()


    def __midpoint(self, p1, p2):
        return (int(((p1[0] + p2[0]) / 2)), int(((p1[1] + p2[1]) / 2)))

    """ This function is responsible for creating middle points of given hands list.
    Mediapipe's hand tracking module returns 21 points on detected hands, but I'm
    interested in inner part of the hand only. """
    def __hands_middle(self, hands = []):
        hands_middle = [[],[]]
        if len(hands[0]) != 0 and len(hands[1]) != 0:
            sumx = 0
            sumy = 0
            for id, hand in enumerate(hands):
                for points in hand:
                    sumx += points[0]    
                    sumy += points[1]
                hands_middle[id].append(int(sumx / len(hands[id])))
                hands_middle[id].append(int(sumy / len(hands[id])))
                sumx = 0
                sumy = 0
        self.middle_of_hands = hands_middle
        

    # This function is used to draw line from bottom to middle in steering wheel
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
        self.__hands_middle(hands)
        if len(hands[0]) != 0 and len(hands[1]) != 0:
            try:
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
            except:
                print("CIRCLE DRAWING ERROR")