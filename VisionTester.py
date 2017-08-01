import numpy as np
import cv2
import math
import sys

import Panoramic
import Radar
import Warp

centerx = 80  #Center of the Image
centery = 60
radius1 = 5   #Inside radius of what to dewarp
radius2 = 60  #Outside radius of what to dewarp

Wd = 2.0*((radius1+radius2)/2)*np.pi #Math for dewarped image's width
Hd = (radius2-radius1)               #Math for dewarped image's height
Ws = 160     #Image capture size from camera
Hs = 120
xmap,ymap = Warp.buildMap(Ws,Hs,Wd,Hd,radius1,radius2,centerx,centery) #Build the array that tells openCV where to move pixels when dewarping

video_capture = cv2.VideoCapture(-1) #"-1" selects any camera, however you can specify with 0-infinity
video_capture.set(3, Ws) #Capture width
video_capture.set(4, Hs) #Capture Height

#Change these two values to run different conencted programs
showVideo = 1
data = 0

while(True):
    if data == 0:
	ret, frame = video_capture.read()
        direction = Panoramic.getBlobAngle(ret, frame, centerx, centery);  #Get the direction of the ball
        radarMap = Radar.drawRadar(direction, 32)                          #Draws a cool radar map with the direction variable
        warp = Warp.unwarp(frame, xmap, ymap)                    #For unwarping the image
    #if data == 1:
	#Put your other openCV algorithms here

    #Quit Key
    if showVideo == 1:
        #cv2.imshow('frame',frame)        #This is the frame as the camera sees it
        cv2.imshow('unwarped', warp)      #This is the unwarped frame
        cv2.imshow('radar',radarMap)      #This is the radar image
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
