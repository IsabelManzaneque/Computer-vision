# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 24/10/2024
Description: Transformaciones Geometricas.

"""

import os
import numpy as np
import cv2

    

def reescalar(img):        
    """
    
       
    """
def afinCompuesta(img):        
    """
    
       
    """           
def transformacionPolar(img):        
    """
    
       
    """
    
def transformacionNoLineal(img):        
    """
    
       
    """
 
def displayResult():    
    """
    Muestra un antes y un después de la imagen modificada      
    
    """
    global originalImg, imgCopy
    res = np.hstack((originalImg,imgCopy))
    cv2.imshow("Antes - Despues", res)
    #cv2.imshow("Original", originalImg)
    #cv2.imshow("Modificada", imgCopy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
operatorDict = {
    
    1 : reescalar,
    2 : afinCompuesta,
    3 : transformacionPolar,
    4 : transformacionNoLineal,
     
    }

#path = input("Introduzca la ruta de la imagen a procesar: ")
path = "C:/Users/Isabe/Desktop/VA/pecs/2024/PEC1/Ejercicio2/assets/zigzag.jpg"
assert os.path.exists(path), "Ruta especificada no existe"
originalImg = cv2.imread(path)
imgCopy = originalImg.copy()    
isROI = False

userInput = ""
while userInput == "":
    print("\n1 - Reescalar")
    print("2 - Transformacion afin compuesta")
    print("3 - Transformacion polar")
    print("4 - Transformacion no lineal")   
    print("5 - Todas las transformaciones")
    print("6 - Mostrar resultado")
    print("7 - Salir")
    try:
        userInput = int(input("Operador a aplicar: "))        
        if userInput == 7:
            print("\nCerrando aplicacion...")
            break
        e userInput in [1,2,3,4,5,6,7]:
            imgCopy = operatorDict[userInput](imgCopy)
            print("\nOperador aplicado correctamente")        
        displayResult()     
    except ValueError as e:
        print("\nError! Introduzca uno de las siguientes opciones: \n")
        print(e)
    finally:
        userInput = ""
        imgCopy = originalImg.copy() 
        print("\nRestableciendo imagen original...")
     
        
     

