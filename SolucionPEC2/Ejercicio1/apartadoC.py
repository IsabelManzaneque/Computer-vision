# -*- coding: utf-8 -*-
"""
File: apartadoE.py
Author: Isabel Manzaneque
Date: 13/12/2023 
Description: Segmentación con conocimiento del dominio.

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

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
    thresh = cv2.threshold(grayImg, 170, 255, cv2.THRESH_BINARY_INV)[1]     
        
    # Deteccion de contornos
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    # Eliminar los contornos de la bounding box
    filteredContours = []
    filteredHierarchy = []      
    
    for i, contour in enumerate(contours):
        rect = cv2.minAreaRect(contour)
        (width, height) = rect[1]
        
        # 100 es un threshold de tamano
        if max(width, height) < 100:
            filteredContours.append(contour)    
            filteredHierarchy.append(hierarchy[0][i][3])
    # Devuelve y dibuja los contornos para visualizacion
    contouredImg = cv2.drawContours(rotatedImg.copy(), filteredContours, -1, (0,255,0), 3)
    
    return contouredImg, filteredContours


# =============================================================================
# def scaleContour(contour, scaleFactorX, scaleFactorY):
#     
#     # Centroide del contorno
#     M = cv2.moments(contour)
#     
#     if M['m00'] != 0:
#         cx = int(M['m10']/M['m00'])
#         cy = int(M['m01']/M['m00'])
#         
#         # Trasladar al origen restando el centro a todos los puntos
#         contourNorm = contour - [cx,cy]
#         
#         # Escalar cada punto del contorno
#         contourScaled = np.column_stack((
#             contourNorm[:, 0, 0] * scaleFactorX,
#             contourNorm[:, 0, 1] * scaleFactorY
#         ))
#         
#         # Devolverlo a su sitio
#         contourScaled = contourScaled + [cx, cy]
#         contourScaled = contourScaled.astype(np.int32)
#         
#         return contourScaled
#     
#     return contour
# =============================================================================

def Normalization1(img, contours) :
    """
    Estire la dimensión más estrecha de la letra para que la 
    dimensión final sea de 20x20.

    """
    letrasNormalizadas = []
    
    for contour in contours:
        # obtener rectangulo delimitador de cada contorno
        x,y,w,h = cv2.boundingRect(contour)
    
        # Recorta y redimensiona la letra a 20 x 20
        letra = img[y:y+h, x:x+w]                
        letraNormalizada = cv2.resize(letra, (20, 20))
        
        letrasNormalizadas.append(letraNormalizada)
     
    return letrasNormalizadas


def Normalization2(img, contours) :
    """
    Ajusta la escala para que la dimensión mayor de la letra sea de 20 píxeles 
    y rellene el espacio en la otra dimensión para que el tamaño final sea de 
    20x20 y la letra esté centrada.
    """
    letrasNormalizadas = []
    
    for contour in contours:
        # obtener rectangulo delimitador de cada contorno
        x,y,w,h = cv2.boundingRect(contour)
    
        # Recorta y redimensiona la letra a 20 x 20
        letra = img[y:y+h, x:x+w]                
        
        h, w = letra.shape[:2]
        
        # Escalar para que la dimensión mayor sea de 20 píxeles
        escala = 20 / max(w, h)
        nuevo_w, nuevo_h = int(w * escala), int(h * escala)
        letra_redimensionada = cv2.resize(letra, (nuevo_w, nuevo_h))
        
        # Calcular el relleno necesario para cada dimensión
        pad_w = (20 - nuevo_w) // 2
        pad_h = (20 - nuevo_h) // 2
        
        
        letraNormalizada = cv2.copyMakeBorder(letra_redimensionada, pad_h, pad_h, pad_w, pad_w, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        
        letrasNormalizadas.append(letraNormalizada)
     
    return letrasNormalizadas


houghLinesImg, meanAngle = drawHoughLines()
rotatedImg = rotate(meanAngle)
# se encuentran los contornos sobre la imagen rotada
contouredImg, contours = segment(rotatedImg)
# se extraen las letras de la imagen rotada
letrasNormalizadas1 = Normalization1(rotatedImg, contours)
letrasNormalizadas2 = Normalization2(rotatedImg, contours)

for letra in letrasNormalizadas2:
    plt.imshow(letra)
    plt.show()

