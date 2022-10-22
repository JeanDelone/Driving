import cv2 as cv
import os
from time import time
from winCapture import WindowCapture

os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture('Forza Horizon 5')
loop_time = time()

while(True):
    main_screen = wincap.get_screenshot()
    main_screen.resize((main_screen.shape[0] // 2, main_screen.shape[1] // 2))
    cv.imshow('FH5', main_screen)

    # debug the loop rate
    print(f'FPS: {int(1 / (time() - loop_time))}')
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


cv.destroyAllWindows


