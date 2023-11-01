# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 01/11/2023
Description: Segmentacion sin conocimiento del dominio.

"""

import cv2
import glob
import os



images = glob.glob(".\\assets\\threshold\\*")

for fname in images:
    # Extension del archivo
    _, extension = os.path.splitext(fname)    

    if extension == '.png':
        
        img = cv2.imread(fname, cv2.IMREAD_GRAYSCALE)
        globalTimg = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)[1]
        adaptativeMean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        adaptativeGaussian = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        
        cv2.imshow("Original", img)
        cv2.imshow("Global", globalTimg)
        cv2.imshow("Adaptive - Median", adaptativeMean)
        cv2.imshow("Adaptive - Gaussian", adaptativeGaussian)
    
    elif extension == '.gif':
        
        gifImg = cv2.VideoCapture(fname)
        _, frame = gifImg.read()
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        globalTimg = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)[1]
        adaptativeMean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        adaptativeGaussian = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
        
        cv2.imshow("Original GIF", img)
        cv2.imshow("Global", globalTimg)
        cv2.imshow("Adaptive - Median", adaptativeMean)   
        cv2.imshow("Adaptive - Gaussian", adaptativeGaussian)
        gifImg.release()

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.destroyAllWindows()

