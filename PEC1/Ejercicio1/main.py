# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 10/10/2024
Description: Eliminación de ruído en imágenes escaneadas.

"""

import os
import numpy as np
import cv2

    
def roiDecorator(func):
    """
    Este decorator permite usar utilizar todas las funciones para la imagen
    completa o para un ROI realizando las siguientes acciones:
        
        - Si el usuario ha seleccionado un ROI, recorta este y lo pasa a la 
          funcion principal. Tras realizar los cambios, lo pega a la imagen y 
          y la devuelve con los cambios sobre el ROI 
    
        - Si el usuario no selecciona una ROI, se pasa a la funcion principal
          la imagen sin recortar y se devuelve con los cambios
       
    """
    def wrapper(img):
        
        global isROI
        roi = None
        
        # Si isROI es True, se recorta el ROI 
        if isROI:            
            x, y, width, height = cv2.selectROI(img)
            roi = img[y:y+height, x:x+width]
            cv2.waitKey(0)
            cv2.destroyAllWindows()        
        
        # A la funcion se pasa la imagen o el ROI 
        changedImg = func(img if isROI is False else roi)
        
        # Si isROI es True se pega el ROI cambiado a la imagen
        if isROI:
            img[y:y+height, x:x+width] = changedImg
            isROI = False
            return img    
        return changedImg
        
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
    while threshold not in range(256):
        try:
            threshold = int(input("Seleccionar un nivel de umbral (0-255): "))
        except ValueError:
            print("Introduzca un valor numérico")
    return cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]

@roiDecorator
def blackFilter(img):
    """
    Función de tipo umbral que recorre los pixeles de la imagen. Si la
    intensidad del pixel es inferior al umbral, establece el pixel a blanco.     
    
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    alto, ancho = img.shape
    
    threshold = ""
    while threshold not in range(256):
        try:
            threshold = int(input("Seleccionar un nivel de umbral (0-255): "))
        except ValueError:
            print("Introduzca un valor numérico")
    
    # Si la intensidad del pixel es menor al umbral 
    # establece el pixel a blanco
    for i in range(alto):
        for j in range(ancho):
            if img[i][j] < threshold:
                img[i][j] = 255   
                
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

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
    cv2.imshow("Antes - Despues", res)
    cv2.imshow("Original", originalImg)
    cv2.imshow("Modificada", imgCopy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

operatorDict = {
    
    1 : nmlFilter,
    2 : medianFilter,
    3 : thresholdFilter,
    4 : blackFilter,
    5 : sharpenImage,
    6 : erode,
    7 : dilate,
    9 : displayResult
  
    }

path = input("Introduzca la ruta de la imagen a procesar: ")
assert os.path.exists(path), "Ruta especificada no existe"
originalImg = cv2.imread(path)
imgCopy = originalImg.copy()    
isROI = False

while True:
    print("\n1 - Filtro Non-Local-Means")
    print("2 - Filtro Mediana")
    print("3 - Filtro Umbralizacion")
    print("4 - Filtro Negro")
    print("5 - Realzar bordes")
    print("6 - Erosionar")
    print("7 - Dilatar")
    print("8 - Seleccionar ROI")
    print("9 - Mostrar resultado")
    print("10 - Restablecer imagen")
    print("11 - Salir")
    try:
        userInput = int(input("Operador a aplicar: "))  
        if userInput < 1 or userInput > 11:
            raise ValueError
        elif userInput in [1,2,3,4,5,6,7]:
            imgCopy = operatorDict[userInput](imgCopy)
            print("\nOperador aplicado con exito") 
        elif userInput == 8:
            isROI = True
            print("\nLa proxima operacion se realizara sobre el ROI")     
        elif userInput == 9:
            operatorDict[userInput]()
        elif userInput == 10:            
            imgCopy = originalImg.copy() 
            print("\nRestablecida imagen original")
        elif userInput == 11:
            print("\nCerrando aplicacion...")
            break               
    except ValueError as e:
        print("\nError! Introduzca un número entre 1 y 11")

     
        
     

