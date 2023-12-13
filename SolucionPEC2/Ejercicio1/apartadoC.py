# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 08:40:22 2023

@author: Isabe
"""

import cv2
import numpy as np


img = cv2.imread(".\\assets\\textoMolinos.png")



def drawHoughLines():
    
    imgCopy = img.copy()
    imgGray = cv2.cvtColor(imgCopy,cv2.COLOR_BGR2GRAY)
    # Detectar los bordes
    edges = cv2.Canny(imgGray,50,150,apertureSize = 3)
    # Detectar lineas usando HoughLines. 
    lines = cv2.HoughLines(edges,1,np.pi/180,228)
    print("lineas detectadas = ", len(lines))
    
    angles = []
    
    for line in lines:
        # theta es la inclinacion de la linea respecto a la horizontal
        rho,theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(imgCopy,(x1,y1),(x2,y2),(0,0,255),2)
        
        # Convertir el angulo a grados y ajustar el rango
        angle = np.rad2deg(theta) - 90
        angles.append(angle)
                
    # Media de las inclinaciones para girar la imagen
    meanAngle = np.mean(angles)  
    
    return imgCopy, meanAngle
  

def rotate(meanAngle):
    
    imgCopy = img.copy()
    height, width = imgCopy.shape[:2]
    imgCenter = (width // 2, height // 2)
    
    rotMatrix = cv2.getRotationMatrix2D(imgCenter, meanAngle, 1)
    return cv2.warpAffine(imgCopy, rotMatrix, (width, height))
    



def segment(rotatedImg):
    
  
    grayImg = cv2.cvtColor(rotatedImg.copy(),cv2.COLOR_BGR2GRAY)   
    #thresh = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]   
    thresh = cv2.threshold(grayImg, 170, 255, cv2.THRESH_BINARY_INV)[1]    
    #thresh = cv2.threshold(grayImg, 170, 255, cv2.THRESH_BINARY)[1]  
    
      
    # Deteccion de contornos
    contours = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[0]
    
    # Eliminar los contornos de la bounding box
    filteredContours = []
    for contour in contours:
        rect = cv2.minAreaRect(contour)
        (width, height) = rect[1]
        
        # 100 es un threshold de tamano
        if max(width, height) < 100:
            filteredContours.append(contour)    
       
    # Devuelve y dibuja los contornos para visualizacion
    contouredImg = cv2.drawContours(rotatedImg.copy(), filteredContours, -1, (0,255,0), 3)
    
    return contouredImg, filteredContours



def scaleContour(contour, scaleFactorX, scaleFactorY):
    
    # Centroide del contorno
    M = cv2.moments(contour)
    
    if M['m00'] != 0:
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        
        # Trasladar al origen restando el centro a todos los puntos
        contourNorm = contour - [cx,cy]
        
        # Escalar cada punto del contorno
        contourScaled = np.column_stack((
            contourNorm[:, 0, 0] * scaleFactorX,
            contourNorm[:, 0, 1] * scaleFactorY
        ))
        
        # Devolverlo a su sitio
        contourScaled = contourScaled + [cx, cy]
        contourScaled = contourScaled.astype(np.int32)
        
        return contourScaled
    
    return contour

def Normalization1(contours) :
    
    imgCopy = img.copy()
    # Crear una imagen en blanco del mismo tamaño que la imagen original
    height, width = imgCopy.shape[:2]
    white_background = np.ones((height, width, 3), dtype=np.uint8) * 255
    
     
    xOffset, yOffset = 0,0
    for contour in contours:
        
        # rectángulo delimitador del contorno
        x, y, w, h = cv2.boundingRect(contour)
        
        # Calcular escala en x e y
        scaleFactorX = 20 / w
        scaleFactorY = 20 / h
        
        # escalar contorno a 20x20 y anadir el desplazamiento
        scaledContour = scaleContour(contour, scaleFactorX, scaleFactorY) 
        scaledContour = scaledContour + (xOffset, yOffset)
        
        # rectangulo del nuevo contorno
        scaledX, scaledY, scaledW, scaledH = cv2.boundingRect(scaledContour)  
       
        # dibujar el contorno
        cv2.drawContours(white_background, [scaledContour], -1, (0, 0, 0), 1)
        
          
        # actualizar el desplazamiento
        
        xOffset, yOffset = 5, 0
        
    return white_background


def Normalization2(contours) :
    
    imgCopy = img.copy()
    # Crear una imagen en blanco del mismo tamaño que la imagen original
    height, width = imgCopy.shape[:2]
    white_background = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Dibujar los contornos en la imagen en blanco
    for contour in contours:
        cv2.drawContours(white_background, [contour], -1, (0, 0, 0))
    
    # Mostrar la imagen
    
    return white_background
        


houghLinesImg, meanAngle = drawHoughLines()
rotatedImg = rotate(meanAngle)
segmentated = segment(rotatedImg)[0]
contours = segment(rotatedImg)[1]


#cv2.imshow("SEGMENTATED", segmentated)
cv2.imshow("NORMALIZATED", Normalization1(contours))
cv2.waitKey(0)
cv2.destroyAllWindows()