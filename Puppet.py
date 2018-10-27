# Avoid Using PyAutoGui as much as you can.(It's slooooooooooooow)
#good work
from collections import deque
import os
from Xlib.display import Display
from Xlib import X
from Xlib.ext.xtest import fake_input
import time
import cv2
import numpy as np
import argparse
import pyautogui
#from pymouse import PyMouse
import math

ap = argparse.ArgumentParser()
ap.add_argument("-b", "--buffer", type=int, default=32, help="max buffer size")
args = vars(ap.parse_args())

yellowLower = (0, 103, 171)
yellowUpper = (65, 255, 255)
# ptsyellow = deque(maxlen=args["buffer"])
redLower = (150, 99, 90)
redUpper = (255, 255, 255)

greenLower = (68, 94, 84)
greenUpper = (85, 255, 255)
# ptsGreen = deque(maxlen=args["buffer"])
counter = 0
arrGreen = [[0, 0]]
# dX, dY = 0, 0
# direction = ""

#m = PyMouse()
flag = 0
_display = Display(os.environ['DISPLAY'])
cap = cv2.VideoCapture(0)
# cap = WebcamVideoStream(src=0).start()
xY ,yY = 0, 0

while True:
    grab, frame = cap.read()
    # frame = cap.read()
    frame = cv2.flip(frame,1)

    frame = cv2.resize(frame, (1366, 768))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    maskYellow = cv2.inRange(hsv, yellowLower, yellowUpper)
    maskYellow = cv2.erode(maskYellow, None, iterations=2)
    maskYellow = cv2.dilate(maskYellow, None, iterations=2)
    
    maskRed = cv2.inRange(hsv, redLower, redUpper)
    maskRed = cv2.erode(maskRed, None, iterations=2)
    maskRed = cv2.dilate(maskRed, None, iterations=2)

    maskGreen = cv2.inRange(hsv, greenLower, greenUpper)
    maskGreen = cv2.erode(maskGreen, None, iterations=2)
    maskGreen = cv2.dilate(maskGreen, None, iterations=2)

    cnts = cv2.findContours(maskYellow.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    cntsRed = cv2.findContours(maskRed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    centerRed = None

    cntsGreen = cv2.findContours(maskGreen.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    centerGreen = None

    if len(cnts) > 0:
        global radius
        c = max(cnts, key=cv2.contourArea)
        ((x,y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        # print x, "||",y,"||", center

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0,255,255), 2)
            cv2.circle(frame, center, 5, (0,0,255), -1)
            #pyautogui.moveTo(center)
            #pyautogui.moveTo(center)
            center = list(center)

            if center[0] % 2 != 0:
                center[0] = center[0] + 1
            if center[1] % 2 != 0:
                center[1] = center[1] + 1

            xY, yY = center
            string = str(xY) + " " + str(yY) + " " + str(int(radius))
            cv2.putText(frame , string, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)
            if xY < 13:
                xY = 0
            if yY < 13:
                yY = 0
            if xY >= 1355:
                xY = 1366
            if yY >= 755:
                yY = 768
            #
            # To move mouse at particular location
            #
            #m.move(xY, yY)
            fake_input(_display, X.MotionNotify, x=xY, y=yY)
            _display.sync()
            print (center)
        # ptsyellow.appendleft(center)
        # print pts

    if len(cntsRed) > 0:
        cRed = max(cntsRed, key=cv2.contourArea)
        ((xRed, yRed), radiusRed) = cv2.minEnclosingCircle(cRed)
        MR = cv2.moments(cRed)
        centerRed = (int(MR["m10"]/MR["m00"]), int(MR["m01"]/MR["m00"]))
        if radiusRed > 10:
            cv2.circle(frame, (int(xRed), int(yRed)), int(radiusRed),(0,255,255), 2)
            cv2.circle(frame, centerRed, 5, (0,255,0), -1)

            xR, yR = centerRed
            string = str(xR) + " " + str(yR) + " " + str(int(radiusRed))            
            cv2.putText(frame , string, (800, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2, cv2.LINE_AA)

# Next 7 lines are for dragging the cursor
# and for single left clicks

        if centerRed is not None and center is not None:
            # pyautogui.mouseDown()
            #m.move(xY, yY)
            fake_input(_display, X.MotionNotify, x=xY, y=yY)
            _display.sync()
            fake_input(_display, X.ButtonPress, 1)
            _display.sync()
        # elif centerRed is not None:
            # fake_input()

    else:
        fake_input( _display,X.ButtonRelease, 1);_display.sync()

    if len(cntsGreen) > 0:
        cGreen = max(cntsGreen, key=cv2.contourArea)
        ((xGreen, yGreen), radiusGreen) = cv2.minEnclosingCircle(cGreen)
        MR = cv2.moments(cGreen)
        centerGreen = (int(MR["m10"]/MR["m00"]), int(MR["m01"]/MR["m00"]))
        if radiusGreen > 10:
            cv2.circle(frame, (int(xGreen), int(yGreen)), int(radiusGreen), (0, 255, 255), 2)
            cv2.circle(frame, centerGreen, 5, (125, 125, 125), -1)
            # ptsGreen.appendleft(centerGreen)
            # counter = counter+1
            arrGreen = np.append(arrGreen, [[centerGreen[0] , centerGreen[1]]], axis = 0)
            # print arrGreen
            if len(arrGreen) == 8:
                if arrGreen[7][1] - arrGreen[1][1] < 0:
                    print ("scroll UP")
                    pyautogui.scroll(2)
                    arrGreen = [[0,0]]
                else:
                    arrGreen = [[0,0]]
                    pyautogui.scroll(-2)
                    print ("scroll Down")


    # for i in np.arange(1, len(ptsGreen)):

    #     if ptsGreen[i-1] is None or ptsGreen[i] is None:
    #         continue

    #     if counter >= 10 and i == 1 and ptsGreen[-10] is not None:

    #         dX = ptsGreen[-10][0] - ptsGreen[i][0]
    #         dY = ptsGreen[-10][1] - ptsGreen[i][1]
    #         dirX , dirY = "" , ""

    #         if np.abs(dY) > 20:
    #             if np.sign(dY) == 1:
    #                 pyautogui.vscroll(5)
    #             else:
    #                 pyautogui.vscroll(-5)

    '''for i in xrange(1, len(ptsred)):

        if ptsred[i-1] is None or ptsred[i] is None:
            continue'''

        # thickness = int(np.sqrt(args["buffer"]/float(i+1))*2.5)
        # cv2.line(frame, pts[i-1], pts[i], (0,0,255), thickness)
        # print pts[i-1]," ", pts[i]

    '''cv2.namedWindow('Frame', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("Frame",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
    cv2.imshow("Frame", frame)'''
    key = cv2.waitKey(60) & 0xFF

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
