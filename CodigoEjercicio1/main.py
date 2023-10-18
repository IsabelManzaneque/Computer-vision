# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 17:46:26 2023

@author: Isabel

-	La aplicación debe tomar una imagen y eliminar el ruido
-	La aplicación toma la ruta de la imagen por consola y la carga
-	Una vez cargada la imagen, se le podrán añadir de forma interactiva y secuencial los operadores de eliminación de ruido
-	La eliminación del ruido puede implicar la aplicación de diferentes operadores

"""

import os
import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt


    
def roiDecorator(func):
    
    def wrapper(imgCopy):
        
        global isROI
        roi = None
        
        if isROI:
            
            x, y, width, height = cv2.selectROI(imgCopy)
            roi = imgCopy[y:y+height, x:x+width]
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        img = imgCopy if isROI is False else roi            
        
        aux = func(img)
        
        if isROI:
            imgCopy[y:y+height, x:x+width] = aux
            isROI = False
            return imgCopy
            
        else:
            return aux
        
    return wrapper

@roiDecorator
def nmlFilter(img):        
    """
    Elimina el ruido tipo "Sal y Pimienta" de una imagen usando Non-Local-Means
    (NML). NML compara bloques de píxeles en una imagen para preservar mejor 
    las estructuras y los bordes, en presencia de ruido.
       
    """
            
    # A mayores valores de filterStrength, mayor filtrado y mayor perdida de detalle
    filterStrength = ""
    while filterStrength == "":
        try:
            filterStrength = int(input("Seleccionar intensidad del filtro: "))
        except ValueError:
            print("Introduzca un valor numérico")
    return cv2.fastNlMeansDenoising(img, None, filterStrength, 7, 21)       

@roiDecorator
def medianFilter(img):
    """
    Elimina el ruido "Sal y Pimienta" de una imagen reemplazando cada píxel con 
    el valor medio de los píxeles vecinos en una ventana definida
    
    """
    windowSize = ""
    while windowSize not in ["3","5","7","9"]:
        windowSize = input("Seleccionar el tamano de la ventana (3,5,7,9): ")        
    return cv2.medianBlur(img, int(windowSize))
    
@roiDecorator
def thresholdFilter(img):
    """
    Convierte una imagen en escala de grises a una imagen binaria. Los píxeles 
    se clasifican como blanco si el valor de su intensidad está por encima del
    umbral y como negro si está por debajo. 
    
    """
    threshold = ""
    while threshold == "":
        try:
            threshold = int(input("Seleccionar un nivel de umbral (0-255): "))
        except ValueError:
            print("Introduzca un valor numérico")
    return cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]

@roiDecorator
def sharpenImage(img):
    """
    Realza los bordes de una imagen aplicando una operación de 
    convolución y un kernel predefinido de realce de bordes.     
    
    """
        
    # kernel de refinado
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
    return cv2.filter2D(img, -1, kernel)       
    
@roiDecorator 
def erode(img):
    """
    Erosiona el dibujo dilatando el fondo     
    
    """
    kernel = np.ones((2,2), np.uint8)  
    return cv2.dilate(img, kernel, iterations=1)

@roiDecorator
def dilate(img):
    """
    Dilata el dibujo erosionando el fondo     
    
    """
    kernel = np.ones((2,2), np.uint8)  
    return cv2.erode(img, kernel, iterations=1)

def displayResult():
    
    """
    Muestra un antes y un después de la imagen modificada      
    
    """
    global originalImg, imgCopy
    res = np.hstack((originalImg,imgCopy))
    cv2.imshow("Result", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

operatorDict = {
    
    1 : nmlFilter,
    2 : medianFilter,
    3 : thresholdFilter,
    4 : sharpenImage,
    5 : erode,
    6 : dilate,
    8 : displayResult
  
    }

path = "C:/Users/Isabe/Desktop/VA/pecs/2024/PEC1/CodigoEjercicio1/DibujosNPT/N_331_JVC_TOTAL-ev1-h.png"
#path = input("Introduzca la ruta de la imagen a procesar: ")
assert os.path.exists(path), "Ruta especificada no existe"
originalImg = cv2.imread(path)
imgCopy = originalImg.copy()    
isROI = False

userInput = ""
while userInput == "":
    print("\n1 - Filtro Non-Local-Means")
    print("2 - Filtro Mediana")
    print("3 - Umbralizacion")
    print("4 - Realzar bordes")
    print("5 - Erosionar")
    print("6 - Dilatar")
    print("7 - seleccionar ROI")
    print("8 - Mostrar resultado")
    print("9 - Salir")
    try:
        userInput = int(input("Operador a aplicar: "))
        
        if userInput == 9:
            print("\nCerrando aplicacion...")
            break
        if userInput == 7:
            isROI = True
            print("\nLa proxima operacion se realizara sobre el ROI")        
        elif userInput in [1,2,3,4,5,6]:
            imgCopy = operatorDict[userInput](imgCopy)
            print("\nOperador aplicado correctamente")        
        else:
            operatorDict[userInput]()       
    except ValueError as e:
        print("\nError! Introduzca uno de las siguientes opciones: \n")
        print(e)
    finally:
        userInput = ""
     
        
     

