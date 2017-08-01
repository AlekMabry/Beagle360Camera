import cv2
import numpy as np
import math

def getBlobAngle(ret, frame, centerx, centery):
    # Gaussian blur
    blur = cv2.GaussianBlur(frame,(5,5),0)

    #Convert to Hue, Saturation, and Value colorspace
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # define range of white color in HSV
    lower_white = np.array([0, 100, 0])
    upper_white = np.array([10, 255, 255])

    # Threshold the HSV image to get only white colors
    thresh = cv2.inRange(hsv, lower_white, upper_white)

    # Find the contours of the frame
    contours,hierarchy = cv2.findContours(thresh.copy(), 1, cv2.CHAIN_APPROX_NONE)

    # Find the biggest contour (if detected)
    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        M = cv2.moments(c)

        #If you are not using the warped view, enable this to draw a rectangle around the object
        #x,y,w,h = cv2.boundingRect(c)
        #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        if M['m00'] != 0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
        else:
            cx = 0
            cy = 0

        #If you are not using the warped view, enable this to draw target lines to the object
        #cv2.line(frame,(cx,0),(cx,720),(255,0,0),1)
        #cv2.line(frame,(0,cy),(1280,cy),(255,0,0),1)

        #Here we are calculating the object's polar coordinates to find direction
	vx = cx-centerx;
        vy = cy-centery;

	magnitude = math.sqrt(math.pow(vx, 2)+math.pow(vy,2))

        #(vnx, vny) is the normalized vec2 of the (x,y) coordinates of the object
	vnx = vx/magnitude
        vny = vy/magnitude

        #Then you use cos inverse to get the angle, however this will always be between
        #0-180, and cannot provide the full 360 angle
        direction = math.degrees(math.acos(vnx))

        #To get the full 360 angle you check if the y value is below the 180 line
        #And reverse the angle, so instead of detecting 0-360 the program detects -180-180
        if (cy < centery):
            direction = -direction
    else:
        direction = 0

    #Enable if you want a dot over the center of the screen to correctly position the mirror
    #cv2.circle(frame, (centerx, centery), 3, (0, 0, 255), -1)

    return direction

    #Enable if you want to draw the direction to the frame
    #font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(frame, str(direction), (10, 120), font, 1, (255, 0, 0), 2)
