import cv2
import numpy as np
import math

def drawRadar(direction, distance):
    img = cv2.imread('Radar_Small.png',1)

    radDir = math.radians(direction)
    xPos = float(distance)*math.cos(radDir)+64.0
    yPos = float(distance)*math.sin(radDir)+64.0
    xFinal = int(xPos)
    yFinal = int(yPos)
    cv2.circle(img, (xFinal, yFinal), 3, (0, 255 , 0), -1)

    return img
