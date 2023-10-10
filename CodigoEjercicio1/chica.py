# -*- coding: utf-8 -*-
"""
Created on Tue Nov  8 10:39:17 2022

@author: Ana Isabel Candón Paños
"""

import cv2 as cv
import numpy as np
import os



# Filtros y funciones

#Filtro de media, los valores serán superiores a 0
def media(imagen):
    valor = 0
    while (valor <= 0):
        try:
            valor = int(input("\nElija un valor para la media." ))
    
        except ValueError:
            print("Por favor, elija un valor válido")
    
    img= cv.blur(imagen, (valor,valor))
    return img


#Filtro gaussiano, los valores serán impares superiores a 1
def gaussiano(imagen):
    valor = 0
    while (valor != 7 and valor != 3 and valor != 5 and valor != 9 and valor != 13 and valor != 11):
        try:
            valor = int(input("\nElija el valor gaussiano. (3,5,7,9,11,13): " ))
    
        except ValueError:
            print("Por favor, elija un valor válido")
       
    img= cv.GaussianBlur(imagen, (valor,valor), 0)
    return img


#Filtro de mediana, los valores serán impares superiores a 1
def mediana(imagen):
    valor = 0
    while (valor != 7 and valor != 3 and valor != 5 and valor != 9 and valor != 13 and valor != 11):
        try:
            valor = int(input("\nElija el valor de desenfoque. (3,5,7,9,11,13): " ))

        except ValueError:
            print("Por favor, elija un valor válido")
      
    img = cv.medianBlur(imagen, valor)
    return img

# umbralización
def umbralizacion(imagen, valorTh, valorSalida):
	valorT, img = cv.threshold(imagen,valorTh,valorSalida,cv.THRESH_BINARY)
	return img

# umbralizacion personalizada
def umbralizacionPersonalizada(imagen):
    correcto = False
    while not correcto:
        try:
            valorTh = int(input("\nElija el valor umbral de los píxeles de entrada (0-negro, 255-blanco): " ))
            valorSalida = int(input("\nElija ahora el valor de salida para los píxeles elegidos (0-negro, 255-blanco): "))
            correcto=True

        except ValueError:
            print("Por favor, elija un valor válido")

    img = umbralizacion(imagen, valorTh, valorSalida)
    return img


# Erosion horizontal
def erosionHorizontal(imagen, tam):
    salida = cv.getStructuringElement(cv.MORPH_RECT, (tam, 1))
    img = cv.erode(imagen,salida)
    return img
    
# Erosion vertical
def erosionVertical(imagen, tam):
     salida = cv.getStructuringElement(cv.MORPH_RECT, (1, tam))
     img = cv.erode(imagen,salida)
     return img
 
# Dilatacion horizontal
def dilatacionHorizontal(imagen, tam):
    salida = cv.getStructuringElement(cv.MORPH_RECT, (tam, 1))
    img = cv.dilate(imagen,salida)
    return img

# Dilatacion horizontal
def dilatacionVertical(imagen, tam):
    salida = cv.getStructuringElement(cv.MORPH_RECT, (1, tam))
    img = cv.dilate(imagen,salida)
    return img

# Erosion general
def erosionar(imagen):
    base = np.ones((3,3), np.uint8) 
    img = cv.dilate(imagen, base) 
    return img

# Dilatacion general
def dilatar(imagen):
    base = np.ones((3,3), np.uint8) 
    img = cv.erode(imagen, base) 
    return img

# Cambio blancos por negros
def blancoNegro(imagen):
    img = 255-imagen
    return img
    

# quitarManchasGrandes
def quitarManchasGrandes(imagen):
    img = blancoNegro(imagen)
    puntos = cv.selectROI("Seleccione el area donde", img, showCrosshair=True, fromCenter=False)
    
    x0 = puntos[0]
    x1 = puntos[1]
    x2 = int(puntos[2]+puntos[0])
    x3 = int(puntos[3]+puntos[1])
    
    ROI = [x0,x1,x2,x3]   
    
    #limpiamos primero lo que se pueda con una función threshold
    imgUmbral = umbralizacion(img, 254, 255)
    
    ##### Hacemos el limpiado de líneas verticales y horizontales
    IHErosion = erosionHorizontal(imgUmbral, 11)
    IVErosion = erosionVertical(imgUmbral, 11)     
    IHDilatacion = dilatacionHorizontal(IHErosion, 11)
    IVDilatacion = dilatacionVertical(IVErosion, 11)
    
    img = 255 - np.maximum(IHDilatacion,IVDilatacion).astype(np.uint8)
    
    imgLimpia =  imagen.copy()      
    imgLimpia[ROI[1]:ROI[3],ROI[0]:ROI[2]] = img[ROI[1]:ROI[3],ROI[0]:ROI[2]]
    
    return imgLimpia
    

#Eliminación de patrones
def quitarPatrones(imagen):
    
    img = blancoNegro(imagen)    
    puntos = cv.selectROI("Seleccione el area donde", img, showCrosshair=True, fromCenter=False)
    
    x0 = puntos[0]
    x1 = puntos[1]
    x2 = int(puntos[2]+puntos[0])
    x3 = int(puntos[3]+puntos[1])
    
    ROI = [x0,x1,x2,x3]
    
    imgUmbral = umbralizacion(img, 10, 255)  
    #para limpiar las pequeñas manchas
    salida = cv.connectedComponentsWithStats(imgUmbral, 8, cv.CV_32S, 5)
    
    numEtiquetas, etiquetas, estadisticas, centros = salida
    
    img = imgUmbral.copy()
    for etiqueta in range(1, numEtiquetas):
       if estadisticas[etiqueta][cv.CC_STAT_AREA] < 20: 
           img[etiquetas == etiqueta] = 0
    
    imagenLimpia =  imagen.copy()
    imgBlanco = 255 - img
    
    imagenLimpia[ROI[1]:ROI[3],ROI[0]:ROI[2]] = imgBlanco[ROI[1]:ROI[3],ROI[0]:ROI[2]]
    
    return imagenLimpia


### funcion para ejecutar lo que el usuario ha pedido
def comenzar(opcion, imgOrig):
    
    if(opcion == "r"):
        opcion = "R"
    elif (opcion == "s"):
        opcion = "S"
    
    switch={
            "1":media,
            "2":mediana,
            "3":gaussiano,
            "4":umbralizacionPersonalizada,
            "5":blancoNegro,
            "6":quitarManchasGrandes,
            "7":quitarPatrones,
            "8":erosionar,
            "9":dilatar,
            "R":revertirCambios,
            "S":salir
            }
    funcionElegida=switch.get(opcion, error)
    
    imgResultado = funcionElegida(imgOrig)
     
    if mostrar:       
        cv.imshow('Imagen entrada', imgOrig)
        cv.imshow('Imagen Resultado', imgResultado)
        cv.waitKey(0)    
        cv.destroyAllWindows()           
        global imgOriginal
        imgOriginal = imgResultado.copy()  

    return 


# Se ha pulsado un 0 salimos
def salir(imgOriginal):
    global mostrar
    global seguir
    seguir = False
    mostrar = False
    print ("\nSaliendo del programa. Hasta pronto!")

# Se ha pulsado una tecla que es errónea
def error(imgOriginal):
    global mostrar
    mostrar = False
    print ("\nOpción no válida\n")

# Devolvemos la imagen a su estado original
def revertirCambios(imagen):
    global mostrar
    mostrar = False
    global imgSinCambios
    global imgOriginal
    imgOriginal = imgSinCambios.copy()
    print ("\nSe han revertido todos los cambios")
    return imgOriginal
    
############################# PROGRAMA EN SÍ #################################

cv.destroyAllWindows()

ruta = input('¿Dónde está tu imagen para procesar?: ')
    
assert os.path.exists(ruta), "No se ha podido encontrar el fichero: " + str(ruta)

imgOriginal = cv.imread(ruta,0)
imgSinCambios = imgOriginal.copy()

mostrar = True
seguir = True
opcion = ""
# MENÚ DE OPCIONES
while (seguir):
    mostrar = True
    print("\n¿Qué operación desea realizar?\n"
          "Pulse 1- Filtro de media\n"
          "Pulse 2- Filtro de mediana\n"
          "Pulse 3- Filtro gaussiano\n"
          "Pulse 4- Aplicar umbralización personalizada\n"
          "Pulse 5- Revertir valores (blancos por negros y viceversa)\n"
          "Pulse 6- Eliminar manchas grandes\n"
          "Pulse 7- Eliminar patrones imagen.\n"
          "Pulse 8- Erosionar.\n"
          "Pulse 9- Dilatar.\n\n"
          "Pulse R- Revertir todos los cambios.\n"
          "Pulse S- Salir.")
    opcion = input("\nElige la opcion que desees: ")
    comenzar(opcion, imgOriginal)

