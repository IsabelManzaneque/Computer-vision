# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 20/12/2023 
Description: Aplicación de reconocimiento de objetos.

"""

import cv2
import glob

def adquisicion():
    """
    Adquiere las imagenes a utilizar
    
    """
    return glob.glob(".\\assets\\*")  
        

def segmentacion(img):
    """
    Aisla las regiones de interes de la imagen
    
    """
    grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY_INV) 
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours
        


def descripcion(img, contours):
    """
    Extracción de caractericas discriminantes para diferenciar
    una cruz griega de otros tipos de cruces

    """
    caracteristicas = []
    
    for i, contour in enumerate(contours):        
                
        M = cv2.moments(contour)
        contourArea = cv2.contourArea(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
                
        # evitar el contorno de la caja        
        if contourArea < 20000 and contourArea > 100:            
                        
            perimeter = cv2.arcLength(contour, True)
            epsilon = 0.0001 * perimeter
            approx = cv2.approxPolyDP(contour, epsilon, True)
            x,y,w,h = cv2.boundingRect(contour)   
            
            # dibuja contorno y rectangulo
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)                        
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)   
            
            # vector de caracteristicas discriminantes
            caracteristicas.append([cx,cy,x,y,w,h])            
                                    
    return img, caracteristicas   
   
   

def reconocimiento(img, caracteristicas):
    """
    Encuentra una correspondencia entre las cruces de la imagen y 
    y el prototipo de cruz griega

    """
    
    # Si el centro del contorno se corresponde con el del rectangulo y 
    # y los lados del rectangulo tienen la misma longitud, es cruz griega
    
    for i, element in enumerate(caracteristicas):        
        
        cx,cy,x,y,w,h = element
        
        cxRect = x + w // 2
        cyRect = y + h // 2
        
        cv2.putText(img, str(i), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1)
        print(f"Figura {i}: abs(w-h): {abs(w-h)}, abs(cx-cxRect): {abs(cx-cxRect)}, abs(cy-cyRect): {abs(cy-cyRect)}  ")
        
        # Umbrales para considerarse cruz griega
        if abs(w-h) < 5 and abs(cx-cxRect) < 7 and abs(cy-cyRect) < 7:
            print(" - Es una cruz griega ")
        else:
            print(" - No es una cruz griega ")
    
    return img



images = adquisicion()
for imgPath in images:
    
    img = cv2.imread(imgPath)    
    
    contornos = segmentacion(img)   
    descrita, caracteristicas =  descripcion(img, contornos)
    resultado = reconocimiento(descrita, caracteristicas)
    
    cv2.imshow("Resultado", resultado)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


