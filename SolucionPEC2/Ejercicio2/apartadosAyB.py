# -*- coding: utf-8 -*-
"""
File: apartadosAyB.py
Author: Isabel Manzaneque
Date: 14/12/2023 
Description: Descriptores de puntos característicos.

"""

import numpy as np
import cv2


formulario = cv2.imread(".\\assets\\formulario.png", 0)
rellenoOriginal = cv2.imread(".\\assets\\formularioRelleno-original.png", 0)
rellenoRotado = cv2.imread(".\\assets\\formularioRelleno-rotado.png", 0)


def orbMatcher(img1, img2):
    """
    Utiliza las caracterticas ORB para encontrar los puntos
    caracterticos y las relaciones entre dos imágenes

    """
    
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
    
    # Draw first 20 matches.
    matchedImg = cv2.drawMatches(img1,kp1,img2,kp2,matches[:20],None, flags=2)
        
    
    return matchedImg, matches, kp1, kp2


def siftMatcher(img1, img2):
    """
    Utiliza las caracterticas SIFT para encontrar los puntos
    caracterticos y las relaciones entre dos imágenes

    """
      
    sift = cv2.SIFT_create()
    
    # find the keypoints and descriptors 
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)
    
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2, k=2)
    
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    processedGood = [item[0] for item in good]
    
    # draws first 20 matches
    matchedImg = cv2.drawMatchesKnn(img1,kp1,img2,kp2,good[:50],None,flags=2)
    
    return matchedImg, processedGood, kp1, kp2

    
def affineTransform(img1, img2, matches, kp1, kp2): 
    """
    Utiliza los puntos caracterticos de dos imágenes para encontrar
    y aplicar la transformación afin que lleva de una imagen a otra

    """
       
    img1KP = []
    img2KP = []

    for match in matches[105:108]:      
        # tomar los key points de img1 y img2
        img1KP.append(kp1[match.queryIdx].pt)
        img2KP.append(kp2[match.trainIdx].pt)

    img1KPnp = np.array([img1KP], dtype=np.float32)
    img2KPnp = np.array([img2KP], dtype=np.float32)    
    
    # mapea los puntos de img2 a los de img1
    T = cv2.getAffineTransform(img2KPnp, img1KPnp)
       
    # aplicar transformacion a imagen 2
    return cv2.warpAffine(img2, T, (img1.shape[1], img1.shape[0]))
  
    

#orbMatchedImg, orbMatches, orbKp1, orbKp2 = orbMatcher(formulario,rellenoRotado)
#orbRotatedImg = affineTransform(formulario,rellenoRotado, orbMatches, orbKp1, orbKp2)

siftMatchedImg, siftMatches, siftKp1, siftKp2 = siftMatcher(formulario,rellenoOriginal)
siftRotatedImg = affineTransform(formulario,rellenoOriginal, siftMatches, siftKp1, siftKp2)


cv2.imshow("Matched", siftMatchedImg)
cv2.imshow("Original", formulario)
cv2.imshow("Afin", siftRotatedImg)
cv2.waitKey(0)
cv2.destroyAllWindows()



