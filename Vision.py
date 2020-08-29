# Copyright Ari Wasch 2020
import cv2 as cv2
import numpy as np
import math


class Vision:

    focalLength = 0.0  # Focal length of largest contour
    angle = 0.0  # Angle of largest contour relative to camera
    fittedHeight = 0.0  # Fitted height of the largest contour
    fittedWidth = 0.0  # Fitted width of the largest contour
    knownWidth = 1.0  # Known Width of object at certain distance in units
    knownHeight = 1.0  # Known height of object at certain distance in units

    def __init__(self, pixelHeight, knownDistance, knownWidth, knownHeight):
        """
        Constructs all the necessary attributes for the Vision object.

        Parameters
        ----------
            pixelHeight : float
                Height of vision target at knownDistance form camera
            knownDistance : float
                Distance of the vision target from camera
            knownWidth : float
                Width of the vision target in units
            knownHeight : float
                Height of the vision target in units
        """

        self.knownWidth = knownWidth
        self.knownHeight = knownHeight

        self.focalLength = (pixelHeight * knownDistance) / knownHeight

    # Calculates distance from 2 coordinates
    def __calculateDistance(self, x1, y1, x2, y2):
        dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return dist

    # returns distance from camera to largest contour
    def getDistance(self):
        if(self.fittedHeight > 0):
            return round(((self.knownHeight * self.focalLength) / self.fittedHeight), 2)
        else:
            return 0

    # Calculates angle based off the difference between theoretical width and
    # actual width
    def getAngle(self):
        ratio = (self.knownWidth / self.knownHeight)
        w2 = self.fittedHeight * ratio
        if(self.knownWidth != 0 and w2 > self.fittedWidth):
            self.angle = (1 - (self.fittedWidth/w2)) * 90
        else:
            self.angle = 0

        return self.angle

    def getFocalLength(self):
        return self.focalLength

    def getFittedBox(self):
        return self.fittedHeight, self.fittedWidth

    def updateFrame(self, frame, low_H, low_S, low_V, high_H, high_S, high_V):
        '''Returns two frames tracking a vision target of HSV values.
           Updates variables related to vision target tracking'''

        color = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        if(low_H > high_H):
            low_H = high_H
        if(low_S > high_S):
            low_S = high_S
        if(low_V > high_V):
            low_V = high_V

        lower = np.array([low_H, low_S, low_V])
        upper = np.array([high_H, high_S, high_V])

        mask = cv2.inRange(hsv, lower, upper)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours
        th, threshed = cv2.threshold(mask, 30, 255, cv2.THRESH_BINARY)
        cnts = cv2.findContours(threshed, cv2.RETR_LIST,  cv2.CHAIN_APPROX_SIMPLE)[-2]

        x = 0
        y = 0
        w = 0
        h = 0

        # Gets data from vision target
        if(len(cnts) > 0):
            c = max(cnts, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(color, [box], 0, (0, 0, 255), 2)

            self.fittedHeight = self.__calculateDistance(box[0][0], box[0][1], box[1][0], box[1][1])
            self.fittedWidth = self.__calculateDistance(box[2][0], box[2][1], box[1][0], box[1][1])

            # Prevents fittedWidth and fittedHeight from swapping
            # print(self.knownHeight)
            if(self.knownHeight > self.knownWidth and self.fittedWidth >
                    self.fittedHeight):
                temp = self.fittedWidth
                self.fittedWidth = self.fittedHeight
                self.fittedHeight = temp
            elif(self.knownWidth > self.knownHeight and self.fittedHeight >
                    self.fittedWidth):
                temp = self.fittedHeight
                self.fittedHeight = self.fittedWidth
                self.fittedWidth = temp

        # Creates frames to track the target
        img = cv2.rectangle(color, (x, y), (x+w, y+h), (0, 255, 0), 2)
        mask = cv2.rectangle(mask, (x, y), (x+w, y+h), (0, 255, 0), 2)

        return mask, img
