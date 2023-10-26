# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 24/10/2024
Description: Transformaciones Geometricas.

"""

import numpy as np
import cv2

def translation(x,y):

    
    return np.matrix([[1,0,x],[0,1,y],[0,0,1]])
    
def scaling(x,y):
    
    return np.matrix([[x,0,0],[0,y,0],[0,0,1]])
    

def rotation(angle):
    
    """
    Devuelve una matriz de rotacion de un angulo pasado como parametro
    
    """
        
    cos = np.cos(np.radians(angle))
    sin = np.sin(np.radians(angle))     
    return np.array([[cos, -sin, 0],[sin, cos, 0],[0, 0, 1]])  

    
    
def shearing(axis, angle):
    """
    
    
    Args:
        - axis: eje sobre el que se desliza la imagen
        - angle: angulo de deslizamiento
    Returns:
        - Matriz de transformacion   
    """
    
    tan = np.tan(np.radians(angle))
    
    if axis == "X":             
        return np.matrix([[1,tan,0],[0,1,0],[0,0,1]])
               
    elif axis == "Y":        
        return np.matrix([[1,0,0],[tan,1,0],[0,0,1]])


    
def reescalarYrotar(img):        
    """
    Aplica un reescalado de 200 x 200 pixels y una rotacion de 45 grados 
    alrededor del su centro a la imagen pasada como parametro. Se reescala
    la imagen de salida 
    
    Args:
        - img: imagen a transformar
    Returns:
        - img: imagen transformada  
    """

    img = cv2.resize(img, (200, 200))
    rotationMatrix = cv2.getRotationMatrix2D((200/2, 200/2), 45, 0.70)        
    return cv2.warpAffine(img, rotationMatrix, (200, 200))
    
def transformacionAfinCompuesta1(img):        
    """
    Implementando las siguientes transformaciones por separado 
    (con matrices de transformación distintas).
    
    T1.- Inclinar 30 grados a la derecha la imagen de entrada 
    T2.- girar 90 grados a la izquierda con centro de giro en el centro de la img
    T3.- Reescalar a la mitad en ambos ejes la imagen obtenida de T2. 
    """   
    
    img = cv2.resize(img, (400, 400))
    rows,cols = img.shape[:2] 
    corners = np.array([[0, 0, 1], [cols, 0, 1], [0, rows, 1], [cols, rows, 1]])    
    
    # Transformacion 1 -----------------------------------------------
    
    shearMatrix = shearMatrix = shearing("X",-30)       
    
    # Calcular las coordenadas de las esquinas después de hacer shear
    shearedCorners = corners @ shearMatrix.T
    
    # Desplazamiento necesario en x e y tras shear 
    xShift = int(max(0, -np.min(shearedCorners[:, 0])))

    translationMatrix = translation(xShift, 0) 
    transShearMatrix =  translationMatrix @ shearMatrix    
    
    img = cv2.warpAffine(img, transShearMatrix[:2, :], (cols+xShift, rows)) 
    
    # Transformacion 2 -------------------------------------------------   
  
    rotationMatrix = rotation(-90) 
    translationMatrix = translation(0, img.shape[1])    
    rotaTransMatrix = translationMatrix @ rotationMatrix

    img = cv2.warpAffine(img, rotaTransMatrix[:2, :], (rows, cols+xShift))  
    
    # Transformacion 3 -------------------------------------------------
    
    scalingMatrix = scaling(0.5,0.5) 
    
    return cv2.warpAffine(img, scalingMatrix[:2, :], (rows//2, (cols+xShift)//2)) 
    
    
    
def transformacionAfinCompuesta2(img):        
    """
    Implementando las transformaciones siguientes en un solo paso (con una 
    única matriz de transformación obtenida por composición de matrices)
    
    T1.- Inclinar 30 grados a la derecha la imagen de entrada 
    T2.- girar 90 grados a la izquierda 
    T3.- Reescalar a la mitad en ambos ejes la imagen obtenida de T2.        
    """   
    img = cv2.resize(img, (400, 400))
    rows,cols = img.shape[:2] 
        
    shearMatrix = shearMatrix = shearing("X",-30)   
    rotationMatrix = rotation(-90) 
    translationMatrix = translation(0, img.shape[1])
    scalingMatrix = scaling(0.5,0.5)  
    
    transformationMatrix =  scalingMatrix @ translationMatrix @ rotationMatrix @ shearMatrix 
    
    return cv2.warpAffine(img, transformationMatrix[:2, :], (rows//2, (cols+230)//2))    
       
       
def transformacionPolar(img):        
    """  
    
       
    """
    rows, cols = img.shape[:2] 
    imgCenter = (cols // 2, rows // 2)
    radius = int(np.sqrt(rows ** 2 + cols ** 2) / 2)    
    
    # Aplicar la transformación log-polar    
    return cv2.warpPolar(img, (360, 360), imgCenter, radius, cv2.WARP_POLAR_LOG)
    
    
    

def deshacerPolar(img):
    """
    """
    
    rows, cols = img.shape[:2]      
    imgCenter = (cols // 2, rows // 2)
    radius = int(np.sqrt(rows ** 2 + cols ** 2) / 2)
    
    polarImg = transformacionPolar(img)
    
    return cv2.warpPolar(polarImg, (cols, rows), imgCenter, radius, cv2.WARP_POLAR_LOG + cv2.WARP_INVERSE_MAP)
    
def transformacionNoLineal(img):        
    """
    
       
    """
    
    # Se puede dividir la imagen original en 2    
  
    height, width = img.shape[:2]    
    firstHalf = img[:, :width//2]
    secondHalf = img[:, width//2:]
    
    # estrechar la mitad izquierda a un tercio
        
    scale = (width*1/3) / (width/2)
    scalingMatrix = scaling(scale, 1)
    firstHalf = cv2.warpAffine(firstHalf, scalingMatrix[:2, :], (int(width * 1/3), height))
    
    # expandir la mitad derecha a 2 tercios
    
    scale = (width*2/3) / (width/2)
    scalingMatrix = scaling(scale, 1)
    secondHalf = cv2.warpAffine(secondHalf, scalingMatrix[:2, :], (int(width * 2/3), height))
    
    return cv2.hconcat([firstHalf, secondHalf])
    
 
def displayResult():    
    """
    Muestra la imagen original y la modificada      
    
    """
    global originalImg, imgCopy
    cv2.imshow("Original", originalImg)
    cv2.imshow("Modificada", imgCopy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
operatorDict = {
    
    1 : reescalarYrotar,
    2 : transformacionAfinCompuesta1,
    3 : transformacionAfinCompuesta2,
    4 : transformacionPolar,
    5 : deshacerPolar,
    6 : transformacionNoLineal,
     
    }


originalImg = cv2.imread("./assets/zigzag.jpg")
imgCopy = originalImg.copy()    

while True:
    print("\n1 - Reescalar y rotar")
    print("2 - Transformacion afin compuesta 1")
    print("3 - Transformacion afin compuesta 2")
    print("4 - Transformacion polar")
    print("5 - Deshacer transformacion polar")
    print("6 - Transformacion no lineal")   
    print("7 - Salir")
    try:
        userInput = int(input("Operador a aplicar: "))        
        if userInput < 1 or userInput > 7:
            raise ValueError("\nError! Introduzca un número entre 1 y 7")
        elif userInput in [1,2,3,4,5,6]:
            imgCopy = operatorDict[userInput](imgCopy)     
            displayResult()  
            imgCopy = originalImg.copy() 
            print("\nRestablecida imagen original")
        elif userInput == 7:
            print("\nCerrando aplicacion...")
            break
    except ValueError as e:
        print("\nError! Introduzca un número entre 1 y 7")
        print(e)
     
        
     

