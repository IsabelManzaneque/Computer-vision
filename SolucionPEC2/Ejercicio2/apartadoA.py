# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 17:25:48 2023

@author: Isabe
"""

import numpy as np
import cv2


formulario = cv2.imread(".\\assets\\formulario.png", 0)
rellenoOriginal = cv2.imread(".\\assets\\formularioRelleno-original.png", 0)
rellenoRotado = cv2.imread(".\\assets\\formularioRelleno-rotado.png", 0)


def orbMatcher(img1, img2):
    
    orb = cv2.ORB_create()    
    
    # find the keypoints and descriptors 
    kp1, des1 = orb.detectAndCompute(img1,None)
    kp2, des2 = orb.detectAndCompute(img2,None)    
    
    # create BFMatcher object
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    
    # Match descriptors.
    matches = bf.match(des1,des2)
    
    # Sort them in the order of their distance.
    matches = sorted(matches, key = lambda x:x.distance)
    
    resultImg = cv2.drawMatches(img1,kp1,img2,kp2,matches[:20],None, flags=2)
    # Draw first 10 matches.    
    
    return resultImg, matches, kp1, kp2


def affineTransform(img1, img2, matches, kp1, kp2):    
   
    img1KP = []
    img2KP = []
 
    # Los mejores son 15:18, 23:26, 24:27, 59:62, 66:69, 71:74
    for match in matches[23:26]:      
        # tomar los key points de img1 y img2
        img1KP.append(kp1[match.queryIdx].pt)
        img2KP.append(kp2[match.trainIdx].pt)

    img1KPnp = np.array([img1KP], dtype=np.float32)
    img2KPnp = np.array([img2KP], dtype=np.float32)    
    
    # mapea los puntos de img2 a los de img1
    T = cv2.getAffineTransform(img2KPnp, img1KPnp)
    
    # aplicar transformacion a imagen 2
    return cv2.warpAffine(img2, T, (img1.shape[1], img1.shape[0]))
  
    

matchedImg, matches, kp1, kp2 = orbMatcher(formulario,rellenoOriginal)
rotatedImg = affineTransform(formulario,rellenoOriginal, matches, kp1, kp2)

cv2.imshow("Matches", matchedImg)
cv2.imshow("rotada", rotatedImg)
cv2.waitKey(0)
cv2.destroyAllWindows()



