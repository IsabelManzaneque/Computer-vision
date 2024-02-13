# -*- coding: utf-8 -*-
"""
File: main.py
Author: Isabel Manzaneque
Date: 24/10/2023
Description: Transformaciones Geometricas.

"""

import numpy as np
import cv2

def translation(x,y):
    """
    Devuelve una matriz de traslacion sobre los ejes x e y

    """    
    return np.matrix([[1,0,x],[0,1,y],[0,0,1]])
    
def scaling(x,y):
    """
    Devuelve una matriz de escalado sobre los ejes x e y

    """        
    return np.matrix([[x,0,0],[0,y,0],[0,0,1]])
    

def rotation(angle):
    
    """
    Devuelve una matriz de rotacion sobre un angulo pasado como parametro
    
    """
        
    cos = np.cos(np.radians(angle))
    sin = np.sin(np.radians(angle))     
    return np.array([[cos, sin, 0],[-sin, cos, 0],[0, 0, 1]])  

    
    
def shearing(axis, angle):
    """
    Devuelve una matriz de cizallamiento sobre un angulo 
    pasado como parametro y un eje del plano
    """
    
    tan = np.tan(np.radians(angle))
    
    if axis == "X":             
        return np.matrix([[1,tan,0],[0,1,0],[0,0,1]])
               
    elif axis == "Y":        
        return np.matrix([[1,0,0],[tan,1,0],[0,0,1]])


    
def escalarYrotar(img):        
    """
    Aplica a la imagen parámetro un reescalado de 200 x 200 pixels, una 
    rotacion de 45 grados alrededor del su centro y un reescalado 1:0.7
    
    """
    
    img = cv2.resize(img, (200, 200))  
       
    scalingMatix = scaling(0.7,0.7)
    rotationMatrix = rotation(45)         
    translationMatrix1 = translation(-200//2, -200/2) 
    translationMatrix2 = translation(200//2, 200/2) 
    
    # Composicion de matrices
    transformationMatrix =  translationMatrix2 @ scalingMatix @ rotationMatrix @ translationMatrix1   
    
    return cv2.warpAffine(img, transformationMatrix[:2, :], (200, 200))


def getXShift(img, shearMatrix):
    """
    Calcula el desplazamiento que se debe aplicar a una imagen tras
    realizar una operacion de shear sobre el eje X para que no 
    perder informacion de la imagen
    """
    rows,cols = img.shape[:2] 
    corners = np.array([[0, 0, 1], [cols, 0, 1], [0, rows, 1], [cols, rows, 1]])
    shearedCorners = corners @ shearMatrix.T
    
    return int(max(0, -np.min(shearedCorners[:, 0])))
    
    
def transformacionAfinCompuesta1(img):        
    """
    Implementa las siguientes transformaciones por separado 
    (con matrices de transformación distintas).
    
    T1.- Inclinar 30 grados a la derecha la imagen de entrada 
    T2.- girar 90 grados a la izquierda con centro de giro en el centro de la img
    T3.- Reescalar a la mitad en ambos ejes la imagen obtenida de T2. 
    """   
    
    img = cv2.resize(img, (400, 400))
    rows,cols = img.shape[:2]        
    
    # Transformacion 1 -----------------------------------------------
    
    shearMatrix = shearing("X",-30)     
    xShift = getXShift(img, shearMatrix)
    translationMatrix = translation(xShift, 0) 
    transShearMatrix =  translationMatrix @ shearMatrix    
    
    img = cv2.warpAffine(img, transShearMatrix[:2, :], (cols+xShift, rows)) 
    
    # Transformacion 2 -------------------------------------------------   
    
    rows,cols = img.shape[:2] 
    
    translationMatrix1 = translation(-cols//2, -rows//2) 
    translationMatrix2 = translation(rows//2, cols//2)   
    rotationMatrix = rotation(90)   
    rotaTransMatrix = translationMatrix2 @ rotationMatrix @ translationMatrix1

    img = cv2.warpAffine(img, rotaTransMatrix[:2, :], (rows, cols)) 
    
    # Transformacion 3 -------------------------------------------------
    
    scalingMatrix = scaling(0.5,0.5) 
    
    return cv2.warpAffine(img, scalingMatrix[:2, :], (rows//2, (cols//2)))     
    
    
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
            
    translationMatrix1 = translation(-cols//2, -rows//2) 
    translationMatrix2 = translation(rows//2, cols//2)   
    shearMatrix = shearMatrix = shearing("X",-30)   
    scalingMatrix = scaling(0.5,0.5)  
    rotationMatrix = rotation(90)    
    xShift = getXShift(img, shearMatrix)
    
    # Composicion de matrices
    transformationMatrix = scalingMatrix @ translationMatrix2 @ rotationMatrix @ translationMatrix1 @ shearMatrix 
    
    return cv2.warpAffine(img, transformationMatrix[:2, :], (rows//2, (cols+xShift)//2))  
       

def rectanguloAobjetivo():
    """
    Genera una imagen sintetica de un rectangulo de lado 40 x 20 sobre un fondo
    y realiza una secuencia de transformaciones para colocarlo en la posicion
    objetivo 
    
    """
    
    # Generar imagen sintetica ------------------------------------------------    

    alto, ancho = 40, 20
    
    background = np.zeros((200,200,3)) 
    rectangle = cv2.rectangle(background,(-ancho//2, -alto//2),(ancho//2,alto//2),(0,255,255),-1)
    
    # Rotar -30 grados y trasladar a centro de masas     
    rotationMatrix = rotation(-30)
    translationMatrix = translation(100,80)
    transformationMatrix = translationMatrix @ rotationMatrix    
    imgBefore = cv2.warpAffine(rectangle, transformationMatrix[:2,:], (200,200))
    
    
    # Transformaciones --------------------------------------------------------    
    
    tM1 = translation(-100, -80)      
    rM = rotation(30)    
    sM = scaling(0.5,0.5)         
    tM = sM @ rM @ tM1
    
    imgAfter = cv2.warpAffine(imgBefore, tM[:2,:], (200,200))

    cv2.imshow('Rectángulo Antes', imgBefore)
    cv2.imshow('Rectángulo Después', imgAfter)    
    cv2.waitKey(0)
    cv2.destroyAllWindows()         
    

def transformacionPolar(img):        
    """  
    Utiliza cv2.warpPolar para obtener una imagen logPolar cuadrada, centrada
    en el centro de la imagen original con una fila por grado y ajustada para 
    ver toda la imagen original. 
       
    """
    rows, cols = img.shape[:2] 
    imgCenter = (cols // 2, rows // 2)
    radius = int(np.sqrt(rows ** 2 + cols ** 2) / 2)    
    
    # Aplicar la transformación log-polar    
    return cv2.warpPolar(img, (360, 360), imgCenter, radius, cv2.WARP_POLAR_LOG)  
       

def deshacerPolar(img):
    """
    Deshace una transformación polar aplicada a una imagen realizando
    la transformación inversa
    """
    
    rows, cols = img.shape[:2]      
    imgCenter = (cols // 2, rows // 2)
    radius = int(np.sqrt(rows ** 2 + cols ** 2) / 2)
    
    polarImg = transformacionPolar(img)
    
    return cv2.warpPolar(polarImg, (cols, rows), imgCenter, radius, cv2.WARP_POLAR_LOG + cv2.WARP_INVERSE_MAP)
    

def transformacionNoLineal(img):        
    """
    Deforma la imagen de manera que su mitad izquierda ocupa 1/3 de la imagen 
    final y la mitad derecha ocupa los 2/3 restantes.       
       
    """
    
    # Divide la imagen original en dos mitades     
  
    height, width = img.shape[:2]    
    firstHalf = img[:, :width//2]
    secondHalf = img[:, width//2:]
    
    # estrecha la mitad izquierda a un tercio
        
    scale = (width*1/3) / (width/2)
    scalingMatrix = scaling(scale, 1)
    firstHalf = cv2.warpAffine(firstHalf, scalingMatrix[:2, :], (int(width * 1/3), height))
    
    # expande la mitad derecha a 2 tercios
    
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
    
    1 : escalarYrotar,
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
    print("7 - Llevar rectangulo a objetivo")
    print("8 - Salir")
    try:
        userInput = int(input("Operador a aplicar: "))        
        if userInput < 1 or userInput > 8:
            raise ValueError
        elif userInput in [1,2,3,4,5,6]:
            imgCopy = operatorDict[userInput](imgCopy)     
            displayResult()  
            imgCopy = originalImg.copy() 
            print("\nRestablecida imagen original")
        elif userInput == 7:
            rectanguloAobjetivo()
        elif userInput == 8:
            print("\nCerrando aplicacion...")
            break
    except ValueError as e:
        print("\nError! Introduzca un número entre 1 y 8")
        
     
        
     

