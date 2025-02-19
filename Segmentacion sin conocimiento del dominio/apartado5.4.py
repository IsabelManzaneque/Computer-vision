# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 06/11/2023
Description: Segmentacion sin conocimiento del dominio - Apartado 5.4
"""

import numpy as np
import cv2 


img = cv2.imread(".\\assets\\brain1.png")
rows, cols = img.shape[:2]
assert img is not None, "file could not be read, check with os.path.exists()"

# Encuentra aproximacion de la materia blanca
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY)

# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations = 2)

# sure background area
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
sure_fg = cv2.threshold(dist_transform,0.22*dist_transform.max(),255,0)[1]

# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)
markers = markers+1
markers[unknown==255] = 0

markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]

cv2.imshow("Background", cv2.resize(sure_bg, (cols//2, rows//2)))
cv2.imshow("Foreground", cv2.resize(sure_fg, (cols//2, rows//2)))
cv2.imshow("Segmentada", cv2.resize(img, (cols//2, rows//2)))
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.destroyAllWindows()