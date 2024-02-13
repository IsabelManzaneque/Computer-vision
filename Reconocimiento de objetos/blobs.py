# -*- coding: utf-8 -*-

"""
File: apartadoA.py
Author: Isabel Manzaneque
Date: 19/12/2023 
Description: Reconocimiento de objetos.

"""
import numpy as np
import cv2


def isCompleteCircle(contour):
    """
    Detecta si un contorno es un circulo completo

    """  

    global img
    
    contourArea = cv2.contourArea(contour)
    (x,y),radius = cv2.minEnclosingCircle(contour)
    center = (int(x),int(y))
    
    # Area circulo 
    circleArea = np.pi*(radius**2)
    
    if circleArea - contourArea < 200:
        img = cv2.circle(img,center,int(radius),(0,255,0),2)
        return True
    return False


def getPercentage(contour):
    """
    Evaluar el porcentaje de cuña faltante respecto al circulo completo
    """
    
    contourArea = cv2.contourArea(contour)
    perimeter = cv2.arcLength(contour, True)
    (x,y),radius = cv2.minEnclosingCircle(contour)
    
    # Area circulo 
    circleArea = np.pi*(radius**2)
    
    # Aproximación poligonal del contorno
    epsilon = 0.001 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    cv2.drawContours(img, [approx], 0, (0, 255, 255), 2) 
    
    diferencia = circleArea - contourArea
    return round(((diferencia / circleArea) * 100),2)
    
    
    
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
    # calcular el perímetro del contorno
    perimeter = cv2.arcLength(contour, True)

    # aproximacion poligonal del contorno
    epsilon = 0.02 * perimeter
    approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # evitar dibujar el contorno de la imagen
    if(len(approx) < 7 and perimeter < 300):
        cv2.drawContours(img, [approx], 0, (255, 255, 0), 2) 
        return len(approx)
    elif perimeter < 300:   
        return len(approx)
    return 0


img = cv2.imread(".\\assets\\blob.jpg")
imgGrayCopy = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)    
ret,thresh = cv2.threshold(imgGrayCopy,220,255,0)
contours,hierarchy = cv2.findContours(thresh, 1, 2)    
circleCounter = InCircleCounter = ellipseCounter = sideCounter = 0

for i, contour in enumerate(contours):     
    
    shape = color = cuna = ""
    
    M = cv2.moments(contour)
    area = cv2.contourArea(contour)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    pixelColor = img[cy, cx][0]
    
    if(pixelColor == 0):
        color = "negro"
    elif(pixelColor < 130):
        color = "gris oscuro"
    elif(pixelColor < 180):
        color = "gris medio"
    else:
        color = "gris claro"
        
    # el contorno de la imagen no nos interesa
    if area < 5000:            
        
        if isCompleteCircle(contour):
            circleCounter += 1  
            shape = "circulo"            
        elif isEllipse(contour):
            ellipseCounter += 1
            shape = "elipse"
        else:
            lados = sideCounterFun(contour)
            if(lados < 7):
                sideCounter += lados
                if lados == 3:
                    shape = "triangulo"
                elif lados == 4:
                    shape = "cuadrado"
                else:
                    shape = "hexagono"
            else:
                InCircleCounter += 1
                sideCounter += 2
                porcentaje = getPercentage(contour)
                shape = "circulo incompleto" 
                cuna = f"Porcentaje que le falta: {porcentaje}%"
                
        print(f"Blob {i} - Forma: {shape}, Area: {area}, Color: {color}. {cuna}")
        cv2.putText(img, str(i), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
    
     
print("\n\nTotal circulos completos: ", circleCounter)
print("Total circulos incompletos: ", InCircleCounter)
print("Total Elipses: ", ellipseCounter)
print("Total Lados: ", sideCounter)       
    
cv2.imshow("Blob", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

    
    
