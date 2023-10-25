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
    

def rotation(angle, rotCenterX, rotCenterY):
    
    """
    Devuelve una matriz de rotacion de un angulo alrededor de un punto
    
    Args:
        - angle: angulo de rotacion
        - rotCenterX: coordenada del eje X sobre la que se va a rotar
        - rotCenterY: coordenada del eje Y sobre la que se va a rotar
    Returns:
        - Matriz de transformacion    
    """
        
    cos = np.cos(np.radians(angle))
    sin = np.sin(np.radians(angle))
    tX = rotCenterX * (1 - cos) + rotCenterY * sin
    tY = rotCenterY * (1 - cos) - rotCenterX * sin
    
    return np.array([[cos, -sin, tX],[sin, cos, tY],[0, 0, 1]])  

    
    
def shearing(axis, angle):
    """
    Devuelve una matriz de rotacion de un angulo alrededor de un punto
    
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
    
def transformacionCompuesta1(img):        
    """
    Implementando las siguientes transformaciones por separado 
    (con matrices de transformación distintas).
    
    T1.- Inclinar 30 grados a la derecha la imagen de entrada 
    T2.- girar 90 grados a la izquierda con centro de giro en el centro de la img
    T3.- Reescalar a la mitad en ambos ejes la imagen obtenida de T2. 
    """   
    
    
    rows,cols = img.shape[:2] 
    esquinas = np.array([[0, 0, 1], [cols, 0, 1], [0, rows, 1], [cols, rows, 1]])
    imgCenterX = (cols-1)/2
    imgCenterY = (rows-1)/2
    
    
    shearMatrix = shearMatrix = shearing("X",-30)        
    rotationMatrix = rotation(-90, imgCenterX, imgCenterY) 
    scalingMatrix = scaling(0.5,0.5)    
    
    # Calcular las coordenadas de las esquinas después de hacer shear
    esquinasSheared = np.dot(esquinas, shearMatrix.T)
    
    # Calcular el desplazamiento que las coordenadas estén dentro de la ventana
    # Calcula las minimas coordenadas X e Y de las coordenadas transformadas
    xShift = int(max(0, -np.min(esquinasSheared[:, 0])))
    yShift = int(max(0, -np.min(esquinasSheared[:, 1])))

    translationMatrix = translation(xShift, 0) 
   
    #Al hacer el shear debemos hacer una traslacion a la derecha
    #Podemos averiguar cuanto debemos desplazar
    tsMatrix = scalingMatrix @ translationMatrix @ shearMatrix
    
    img = cv2.warpAffine(img, tsMatrix[:2, :], (cols, rows))      
    #img = cv2.warpAffine(img, rotationMatrix[:2, :], (cols, rows))      
    #img = cv2.warpAffine(img, scalingMatrix[:2, :], (rows//2, cols//2)) 
    
    return img
    
def transformacionCompuesta2(img):        
    """
    Implementando las transformaciones siguientes en un solo paso (con una 
    única matriz de transformación obtenida por composición de matrices)
    
    T1.- Inclinar 30 grados a la derecha la imagen de entrada 
    T2.- girar 90 grados a la izquierda 
    T3.- Reescalar a la mitad en ambos ejes la imagen obtenida de T2.        
    """   
    rows,cols = img.shape[:2] 
    imgCenterX = (cols-1)/2
    imgCenterY = (rows-1)/2  
    

    shearMatrix = shearMatrix = shearing("X",-30)     
    rotationMatrix = rotation(-90, imgCenterX, imgCenterY) 
    scalingMatrix = scaling(0.5,0.5)   
    
    # Matriz de transformacion 
    transformationMatrix =  scalingMatrix @ rotationMatrix @ shearMatrix  
    img = cv2.warpAffine(img, transformationMatrix[:2, :], (rows//2, cols//2))
    
    return img
       
       
def transformacionPolar(img):        
    """
    
       
    """
    pass
    
def transformacionNoLineal(img):        
    """
    
       
    """
    pass
 
def displayResult():    
    """
    Muestra un antes y un después de la imagen modificada      
    
    """
    global originalImg, imgCopy
    #res = np.hstack((originalImg,imgCopy))
    #cv2.imshow("Antes - Despues", res)
    #cv2.imshow("Original", originalImg)
    cv2.imshow("Modificada", imgCopy)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
operatorDict = {
    
    1 : reescalarYrotar,
    2 : transformacionCompuesta1,
    3 : transformacionCompuesta2,
    4 : transformacionPolar,
    5 : transformacionNoLineal,
     
    }


originalImg = cv2.imread("./assets/zigzag.jpg")
imgCopy = originalImg.copy()    

while True:
    print("\n1 - Reescalar y rotar")
    print("2 - Transformacion afin compuesta 1")
    print("3 - Transformacion afin compuesta 2")
    print("4 - Transformacion polar")
    print("5 - Transformacion no lineal")   
    print("6 - Salir")
    try:
        userInput = int(input("Operador a aplicar: "))        
        if userInput < 1 or userInput > 6:
            raise ValueError("\nError! Introduzca un número entre 1 y 5")
        elif userInput in [1,2,3,4,5]:
            imgCopy = operatorDict[userInput](imgCopy)     
            displayResult()  
            imgCopy = originalImg.copy() 
            print("\nRestablecida imagen original")
        elif userInput == 6:
            print("\nCerrando aplicacion...")
            break
    except ValueError as e:
        print("\nError! Introduzca un número entre 1 y 5")
        print(e)
     
        
     

