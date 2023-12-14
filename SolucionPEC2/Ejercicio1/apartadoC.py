# -*- coding: utf-8 -*-
"""
File: apartadoE.py
Author: Isabel Manzaneque
Date: 13/12/2023 
Description: Segmentación con conocimiento del dominio.

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
    #thresh = cv2.threshold(grayImg, 170, 255, cv2.THRESH_BINARY_INV)[1]    
    #thresh = cv2.threshold(grayImg, 170, 255, cv2.THRESH_BINARY)[1]      
    
    # si usas esto no uses threshold y pasale edges a findContours
    blurredImg = cv2.GaussianBlur(grayImg, (5, 5), 0)
    edges = cv2.Canny(blurredImg, 50, 150)
                      
                      
    # Deteccion de contornos
    contours, h = cv2.findContours(edges, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    # Eliminar los contornos de la bounding box
    filteredContours = []
    filteredh = []
    
    for i, contour in enumerate(contours):
        rect = cv2.minAreaRect(contour)
        (width, height) = rect[1]
        
        # 100 es un threshold de tamano
        if max(width, height) < 100:
            filteredContours.append(contour)    
            filteredh.append(h[0][i][3])
    # Devuelve y dibuja los contornos para visualizacion
    contouredImg = cv2.drawContours(rotatedImg.copy(), filteredContours, -1, (0,255,0), 3)
    
    return contouredImg, filteredContours, filteredh



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

def Normalization1(contours, j) :
    """
    Estire la dimensión más estrecha de la letra para que la 
    dimensión final sea de 20x20.

    """
    imgCopy = img.copy()
    # Crear una imagen en blanco del mismo tamaño que la imagen original
    height, width = imgCopy.shape[:2]
    white_background = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    #contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])
    
    for contour in contours:
        

        # rectángulo delimitador del contorno
        x, y, w, h = cv2.boundingRect(contour)

        # Calcular escala en x e y
        scaleFactorX = 20 / w
        scaleFactorY = 20 / h
        
        # escalar contorno a 20x20 y anadir el desplazamiento
        scaledContour = scaleContour(contour, scaleFactorX, scaleFactorY) 
        #scaledContour = scaledContour + (xOffset, yOffset)
        
        # rectangulo del nuevo contorno
        scaledX, scaledY, scaledW, scaledH = cv2.boundingRect(scaledContour)  
        cv2.drawContours(white_background, [scaledContour], -1, (0, 0, 0), 1)         
            
        
    return white_background


def Normalization2(contours) :
    """
    Ajusta la escala para que la dimensión mayor de la letra sea de 20 píxeles 
    y rellene el espacio en la otra dimensión para que el tamaño final sea de 
    20x20 y la letra esté centrada.
    """
    imgCopy = img.copy()
    # Crear una imagen en blanco del mismo tamaño que la imagen original
    height, width = imgCopy.shape[:2]
    white_background = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Dibujar los contornos en la imagen en blanco
    for contour in contours:
        cv2.drawContours(white_background, [contour], -1, (0, 0, 0))
    
    # Mostrar la imagen
    
    return white_background



   
def Normalization3(rotatedImg, contours) :     
    
    imgCopy = rotatedImg.copy()
    height, width = imgCopy.shape[:2]
    white_background = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    
    for contour in contours:
        
        
        x, y, w, h = cv2.boundingRect(contour)
        imgCrop = imgCopy[y:y+h, x:x+w]
        
        scaleFactorX = 20 / w
        scaleFactorY = 20 / h
        
        imgResized = cv2.resize(imgCrop, (0,0), fx=scaleFactorX, fy=scaleFactorY)  
        
        # Calculate the position to place imgResized (e.g., centering it within the bounding box)
        offsetX = x + (w - imgResized.shape[1]) // 2
        offsetY = y + (h - imgResized.shape[0]) // 2

        # Place imgResized onto white_background
        white_background[offsetY:offsetY+imgResized.shape[0], offsetX:offsetX+imgResized.shape[1]] = imgResized

    return white_background

houghLinesImg, meanAngle = drawHoughLines()
rotatedImg = rotate(meanAngle)
segmentated = segment(rotatedImg)[0]
contours = segment(rotatedImg)[1]
h = segment(rotatedImg)[2]


cv2.imshow("NORMALIZATED", Normalization1(contours, h))
cv2.waitKey(0)
cv2.destroyAllWindows()