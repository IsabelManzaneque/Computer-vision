# -*- coding: utf-8 -*-
"""
File: apartadoC.py
Author: Isabel Manzaneque
Date: 13/12/2023 
Description: Segmentación con conocimiento del dominio.

"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread(".\\assets\\textoMolinos.png")



def drawHoughLines():
    """
    Aplica la transformada de Hough a la deteccion de la direccion 
    del texto en la imagen
    """
    imgCopy = img.copy()
    imgGray = cv2.cvtColor(imgCopy,cv2.COLOR_BGR2GRAY)
    # Detectar los bordes
    edges = cv2.Canny(imgGray,50,150,apertureSize = 3)
    # Detectar lineas usando HoughLines. 
    lines = cv2.HoughLines(edges,1,np.pi/180,228)    
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
    """
    Realiza una transformacion afin que rota la imagen para que
    las lineas queden en horizontal
    """
    imgCopy = img.copy()
    height, width = imgCopy.shape[:2]
    imgCenter = (width // 2, height // 2)
    
    rotMatrix = cv2.getRotationMatrix2D(imgCenter, meanAngle, 1)
    return cv2.warpAffine(imgCopy, rotMatrix, (width, height))


def segment(rotatedImg):
    """
    Realiza la segmentacion del texto en la imagen rotada. Obtiene
    y devuelve los contornos del texto para que sean utilizados
    en las funciones de normalizacion

    """
  
    grayImg = cv2.cvtColor(rotatedImg.copy(),cv2.COLOR_BGR2GRAY)      
    thresh = cv2.threshold(grayImg, 170, 255, cv2.THRESH_BINARY_INV)[1]     
        
    # Deteccion de contornos externos    
    contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]    
    
    filteredContours = []
    
    for contour in contours:
        
        contourArea = cv2.contourArea(contour)               
        # Eliminar los contornos de la bounding box
        if contourArea < 1000:
            filteredContours.append(contour)    
           
    # Devuelve y dibuja los contornos para visualizacion
    contouredImg = cv2.drawContours(rotatedImg.copy(), filteredContours, -1, (0,255,0), 3)
    
    return contouredImg, filteredContours


def normalization1(img, contours):
    """
    Estira la dimensian mas estrecha de la letra para que la 
    dimensian final sea de 20x20

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


def normalization2(img, contours) :
    """
    Ajusta la escala para que la dimensión mayor de la letra sea de 20 píxeles 
    y rellene el espacio en la otra dimensión para que el tamaño final sea de 
    20x20 y la letra esté centrada.
    """
    letrasNormalizadas = []
    
    for contour in contours:
        # obtener rectangulo delimitador de cada contorno
        x,y,w,h = cv2.boundingRect(contour)
    
        # recorta la letra
        letra = img[y:y+h, x:x+w]           
        h, w = letra.shape[:2]
        
        # escalar para que la dimension mayor sea de 20 pixeles
        scaleFactor = 20 / max(w, h)
        scaledW, scaledH = int(w * scaleFactor), int(h * scaleFactor)
        letra_redimensionada = cv2.resize(letra, (scaledW, scaledH))
        
        # calcular el relleno para la dimension menor
        padW = (20 - scaledW) // 2
        padH = (20 - scaledH) // 2        
        
        letraNormalizada = cv2.copyMakeBorder(letra_redimensionada, padH, padH, padW, padW, cv2.BORDER_CONSTANT, value=[255, 255, 255])
        
        letrasNormalizadas.append(letraNormalizada)
     
    return letrasNormalizadas


houghLinesImg, meanAngle = drawHoughLines()
rotatedImg = rotate(meanAngle)
# se encuentran los contornos sobre la imagen rotada
contouredImg, contours = segment(rotatedImg)
# se extraen las letras de la imagen rotada
letrasNormalizadas1 = normalization1(rotatedImg, contours)
letrasNormalizadas2 = normalization2(rotatedImg, contours)

    
for letra in letrasNormalizadas2:
    plt.imshow(letra)
    plt.show()

