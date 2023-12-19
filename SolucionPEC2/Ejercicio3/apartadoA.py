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
IncompleteCircleCounter = 0
ellipseCounter = 0
sideCounter = 0
porcentajes = []

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

def isIncompleteCircle(contour):
    """
    Evaluar el porcentaje de cuña faltante respecto al circulo completo
    """
    
    contourArea = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    (x,y),radius = cv2.minEnclosingCircle(contour)
    radius = int(radius)
    circleArea = np.pi*(radius**2)    
    
    # Aproximación poligonal del contorno
    epsilon = 0.001 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    cv2.drawContours(img, [approx], 0, (0, 255, 255), 2) 
    
    diferencia = circleArea - contourArea
    porcentaje = round(((diferencia / circleArea) * 100),2)
    porcentajes.append(porcentaje)
    
    
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
        img = cv2.ellipse(img, ellipse, (0, 0, 255), 2)  
        return True
    
    return False
    

def sideCounterFun(contour):
    """
    Evalua el numero de lados rectos del contorno

    """
    
    # Calcular el perímetro del contorno
    perimeter = cv2.arcLength(contour, True)

    # Aproximación poligonal del contorno
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # evitar dibujar el contorno de la imagen
    if(len(approx) < 7 and perimeter < 300):
        cv2.drawContours(img, [approx], 0, (255, 255, 0), 2) 
        return len(approx)
    elif perimeter < 300:   
        return len(approx)
    return 0

    
    
for i, contour in enumerate(contours):     
         
    if isCompleteCircle(contour):
        circleCounter += 1  
        ## detectar color y tamano aqui?
    elif isEllipse(contour):
        ellipseCounter += 1
    else:
        lados = sideCounterFun(contour)
        if(lados < 7):
            sideCounter += lados
        else:
            IncompleteCircleCounter += 1
            isIncompleteCircle(contour)
    
    
print("Total circulos completos: ", circleCounter)
print("Total circulos incompletos: ", IncompleteCircleCounter)
print("Total Elipses: ", ellipseCounter)
print("Total Lados: ", sideCounter)   

for i, porcentaje in enumerate(porcentajes):
    print(f"El porcentaje de cuña que le falta al semicirculo {i+1} es {porcentaje}%")
    
    
cv2.imshow("Blob", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

    
    
