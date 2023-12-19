# -*- coding: utf-8 -*-

"""
File: apartadoA.py
Author: Isabel Manzaneque
Date: 19/12/2023 
Description: Reconocimiento de objetos.

"""
import numpy as np
import cv2


img = cv2.imread(".\\assets\\blob.jpg")
imgGrayCopy = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
ret,thresh = cv2.threshold(imgGrayCopy,225,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)
circleCounter = 0
ellipseCounter = 0
sideCounter = 0


def isCompleteCircle(contour):
    """
    Detecta si un contorno es un circulo completo

    """
    global img
    
    contourArea = cv2.contourArea(contour)
    (x,y),radius = cv2.minEnclosingCircle(contour)
    center = (int(x),int(y))
    radius = int(radius)
    
    # Area circulo    
    circleArea = np.pi*(radius**2)
    
    # Si la diferencia entre el area del contorno y la del circulo minimo 
    # es menor al 3.5% minimo, el contorno se considera un círculo.
    if (circleArea - contourArea <  circleArea * 0.035) :
        img = cv2.circle(img,center,radius,(0,255,0),2)
        return True
    
    return False  

def isEllipse(contour):
    """
    Detecta si un contorno es una elipse

    """
    global img
    
    # cv2.fitEllipse requiere que el contorno tenga al menos 5 puntos
    if len(contour) < 5:
        return False
    
    contourArea = cv2.contourArea(contour)
    ellipse = cv2.fitEllipse(contour)
    (x, y), (MA, ma), angle = ellipse
    
    # Area elipse    
    ellipseArea = np.pi*(MA/2)*(ma/2)

    if abs(contourArea - ellipseArea) < 0.010 * ellipseArea:
        img = cv2.ellipse(img, ellipse, (0, 255, 0), 2)  
        return True
    
    return False
    

for contour in contours:
    
    M = cv2.moments(contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    
    
    # dibuja centroide del blob
    img=cv2.circle(img,(cx,cy),1, (0, 0, 255), 2)  
    
         
    if isCompleteCircle(contour):
        circleCounter += 1        
    elif isEllipse(contour):
        ellipseCounter += 1
        
    
    
print("Circulos completos: ", circleCounter)
print("Elipses: ", ellipseCounter)
    
 
cv2.imshow("Blob", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

    
    
# =============================================================================
#     # bounding rectangle
#     x,y,w,h = cv2.boundingRect(contour)
#     img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#     
#     # rotated rectangle
#     rect = cv2.minAreaRect(contour)
#     box = cv2.boxPoints(rect)
#     box = np.int0(box)
#     img = cv2.drawContours(img,[box],0,(0,0,255),2)
# 
   

#     
#     # line
#     rows,cols = img.shape[:2]
#     [vx,vy,x,y] = cv2.fitLine(contour, cv2.DIST_L2,0,0.01,0.01)
#     lefty = int((-x*vy/vx) + y)
#     righty = int(((cols-x)*vy/vx)+y)
#     img = cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)
# =============================================================================


