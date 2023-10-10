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

    

def removeSaltPepper():        
    """
    Borra el ruido tipo "Sal y Pimienta" de una imagen usando 
    Non-Local-Means (NML). NML compara bloques de píxeles en una 
    imagen para preservar mejor las estructuras y los bordes, 
    en presencia de ruido.
       
    """
            
    global imgCopy
    # A mayores valores de filterStrength, mayor filtrado y mayor perdida de detalle
    filterStrength = ""
    while filterStrength == "":
        try:
            filterStrength = int(input("Seleccionar intensidad del filtro: "))
        except ValueError:
            print("Introduzca un valor numérico")
    imgCopy = cv2.fastNlMeansDenoising(imgCopy, None, filterStrength, 7, 21)       

def removeColoredLines():
    
    global imgCopy
    # all pixels value above 50 will be set to 255 
    _, imgCopy = cv2.threshold(imgCopy, 165, 255, cv2.THRESH_BINARY)

def sharpenImage():
    """
    Realza los bordes de una imagen aplicando una operación de 
    convolución y un kernel predefinido de realce de bordes.     
    
    """
        
    global imgCopy
    # kernel de refinado
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]) 
    imgCopy = cv2.filter2D(imgCopy, -1, kernel)       
    

def displayResult():
    
    """
    Muestra una comparacion de la imagen original con la modificada     
    
    """
    global originalImg, imgCopy
    res = np.hstack((originalImg,imgCopy))
    cv2.imshow("Result", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    


operatorDict = {
    
    1 : removeSaltPepper,
    2 : removeColoredLines,
    3 : sharpenImage,
    4 : displayResult,
  
    }

path = "C:/Users/Isabe/Desktop/VA/pecs/2024/PEC1/CodigoEjercicio1/DibujosNPT/N_331_JVC_TOTAL-ev1-h.png"
#path = input("Introduzca la ruta de la imagen a procesar: ")
assert os.path.exists(path), "Ruta especificada no existe"
originalImg = cv2.imread(path)
imgCopy = originalImg.copy()    

userInput = ""
while userInput == "":
    print("1 - Eliminar ruido 'Sal y Pimienta'")
    print("2 - Eliminar lineas")
    print("3 - Realzar bordes")
    print("4 - Mostrar resultado")
    print("5 - Salir")
    try:
        userInput = int(input("Operador a aplicar: "))
        if userInput == 5:
            print("\nCerrando aplicacion...")
            break
        operatorDict[userInput]()
    except ValueError as e:
        print("\nError! Introduzca uno de las siguientes opciones: \n")
    finally:
        userInput = ""
     
        
     


# =============================================================================
#     edges = cv2.Canny(denoised_img, threshold1=30, threshold2=100)    
#     mask = np.zeros_like(denoised_img)
#     mask[edges != 0] = 255   
#     restored_image = denoised_img.copy()
#     restored_image[mask != 0] = 255
# =============================================================================


# 4.subir la linea al centro de ambos ojos

# =============================================================================
# def howIs(image):
#     print("-------------------------------------------")
#     print(str(image))
#     print("size = ", image.shape)
#     print("max = ", np.max(image))
#     print("min = ", np.min(image))
#     
# def segmenta(image, umbral):
#     (n,m) = image.shape
#     outputImage = np.zeros((n,m))
#     for i in range(n):
#         for j in range(m):
#             if image[i,j] > umbral:
#                 outputImage[i,j] = 255
#     return outputImage
#             
#     
#     
# img = cv2.imread("assets/onerice.bmp")
# 
# x = img[:,:,0]
# y = segmenta(x, 140)
#plt.imshow(y)  
# =============================================================================

