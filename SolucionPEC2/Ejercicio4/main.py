# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 20/12/2023 
Description: Aplicación de reconocimiento de objetos.

"""

import cv2
import numpy as np
import glob

def adquisicion():
    #return glob.glob(".\\assets\\*")
  
    return cv2.imread(".\\assets\\cruces.jpg")
        

def preprocesado(img):
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    kernel = np.ones((3,3), np.uint8)
    dilated_edges = cv2.dilate(edges, kernel, iterations=1)
    closed_edges = cv2.erode(dilated_edges, kernel, iterations=1)
    
    return closed_edges


def segmentacion(img):
    
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY_INV) 
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours
    
    


def descripcion(img, contours):
    
    
    for i, contour in enumerate(contours):
        
        M = cv2.moments(contour)
        contourArea = cv2.contourArea(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
                
        # evitar el contorno de la caja        
        if contourArea < 20000 and contourArea > 100:
            
            cv2.putText(img, str(i), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
            
            perimeter = cv2.arcLength(contour, True)
            epsilon = 0.0001 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)  
            
            x,y,w,h = cv2.boundingRect(contour)
            cxRect = x + w // 2
            cyRect = y + h // 2
               
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            
            # Si el centro del contorno se corresponde con el del rectangulo y 
            # y los lados del rectangulo tienen la misma longitud, es cruz griega
            
            print(f"Contorno {i}: abs(w-h): {abs(w-h)}, abs(cx-cxRect): {abs(cx-cxRect)}, abs(cy-cyRect): {abs(cy-cyRect)}  ")
            
            if abs(w-h) < 5 and abs(cx-cxRect) < 3 and abs(cy-cyRect) < 3:
                print(f"Contorno {i}: es una cruz griega ")
                        
    return img


    
   
   

def reconocimiento():
    pass



img = adquisicion()

    
contornos = segmentacion(img)   
descrita =  descripcion(img, contornos)

cv2.imshow("result", cv2.resize(descrita, None, fx=0.8, fy=0.8))
#cv2.imshow("Resultado", descrita)
cv2.waitKey(0)
cv2.destroyAllWindows()


# =============================================================================
# images = adquisicion()
# for imgPath in images:
#     
#     img = cv2.imread(imgPath)
#     processedImg = segmentacion(img)    
#     cv2.imshow("Resultado", processedImg)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()
# =============================================================================

