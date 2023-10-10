# -*- coding: utf-8 -*-
"""
@author: Alberto Martínez Montenegro
"""
import os
import cv2 
import numpy as np

def filtroMediana(): 
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    imagenPreviaALaUltimaOperacion = imagenResultado.copy()
    n = ""
    while (n != "3" and n != "5" and n != "7" and n != "9"):
        print("¿Cántos pixeles vecinos (N) se tendrán en cuenta para calcular la mediana?\n"
          "3\n"
          "5\n"
          "7\n"
          "9\n")
        n = input("Selecciona una de las opciones:")
    imagenResultado= cv2.medianBlur(imagenPreviaALaUltimaOperacion, int(n))
    print ("\033[31m Se ha aplicado filtro de mediana. \033[m")

def filtroColorRGB(): 
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    imagenPreviaALaUltimaOperacion = imagenResultado.copy() 
    alto=imagenResultado.shape[0]
    ancho=imagenResultado.shape[1]
    r = int(input("Introduce el valor para RED (0-255):"))
    g = int(input("Introduce el valor para GREEN (0-255):"))
    b = int(input("Introduce el valor para BLUE (0-255):"))
    for x in range (alto):
        for y in range (ancho):
            if imagenResultado.item(x, y, 0)==b and imagenResultado.item(x, y, 1)==g and imagenResultado.item(x, y, 2)==r:
                imagenResultado.itemset((x, y, 0), 255)
                imagenResultado.itemset((x, y, 1), 255)
                imagenResultado.itemset((x, y, 2), 255)
    print ("\033[31m Se ha aplicado filtro RGB. \033[m")

def fltroBlancoYNegro():
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    imagenPreviaALaUltimaOperacion = imagenResultado.copy() 
    roi = cv2.selectROI(imagenResultado)
    roi = imagenResultado[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    alto=roi.shape[0]
    ancho=roi.shape[1]
    for x in range (alto):
        for y in range (ancho):
            if roi.item(x, y, 0)!=0 or roi.item(x, y, 1)!=0 or roi.item(x, y, 2)!=0:
                roi.itemset((x, y, 0), 255)
                roi.itemset((x, y, 1), 255)
                roi.itemset((x, y, 2), 255)
    roi[:] = roi
    print ("\033[31m Se ha aplicado filtro Blanco y Negro. \033[m")

def suavizadoBordes():
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    imagenPreviaALaUltimaOperacion = imagenResultado.copy()
    roi = cv2.selectROI(imagenResultado)
    roi = imagenResultado[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    roi[:] = cv2.blur(roi,(3,3),cv2.BORDER_DEFAULT)

def erosionar():
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    imagenPreviaALaUltimaOperacion = imagenResultado.copy()
    kernel = np.ones((2,2), np.uint8) 
    roi = cv2.selectROI(imagenResultado)
    roi = imagenResultado[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    roi[:] = cv2.dilate(roi, kernel) 
    print ("\033[31m Se ha erosionado la ROI. \033[m")

def dilatar():
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    imagenPreviaALaUltimaOperacion = imagenResultado.copy()
    kernel = np.ones((2,2), np.uint8) 
    roi = cv2.selectROI(imagenResultado)
    roi = imagenResultado[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    roi[:] = cv2.erode(roi, kernel) 
    print ("\033[31m Se ha dilatado la ROI. \033[m")

def guardarImagenEsqueleto():
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    global imagenEsqueleto
    imagenPreviaALaUltimaOperacion = imagenResultado.copy()
    imagenTemporal= cv2.bitwise_not(imagenResultado)
    imagenTemporal = cv2.cvtColor(imagenTemporal, cv2.COLOR_BGR2GRAY)
    skel = imagenTemporal.copy()
    skel[:,:] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3,3))
    cont = 0
    while True:
        eroded = cv2.morphologyEx(imagenTemporal, cv2.MORPH_ERODE, kernel)
        temp = cv2.morphologyEx(eroded, cv2.MORPH_DILATE, kernel)
        temp  = cv2.subtract(imagenTemporal, temp)
        skel = cv2.bitwise_or(skel, temp)
        imagenTemporal[:,:] = eroded[:,:]
        cont = cont +1
        if cv2.countNonZero(imagenTemporal) == 0 or cont >20000 :
            break
    imagenEsqueleto = cv2.bitwise_or(imagenTemporal, cv2.bitwise_not(skel))
    print ("\033[31m Esqueleto guardado con éxito. \n \033[m")   
    
def recuperarImagenEsqueleto():
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    global imagenEsqueleto
    imagenPreviaALaUltimaOperacion = imagenResultado.copy() 
    roi = cv2.selectROI(imagenResultado)
    w=int(roi[0])
    z=int(roi[1])
    roi = imagenResultado[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
    alto=roi.shape[0]
    ancho=roi.shape[1]
    for x in range (alto):
        for y in range (ancho):
            if imagenEsqueleto.item(x + z, y + w)!=255:
                roi.itemset((x, y, 0), 0)
                roi.itemset((x, y, 1), 0)
                roi.itemset((x, y, 2), 0)
    roi[:] = roi
    print ("\033[31m Se ha recompuesto la imagen utilizando el esqueleto guardadoo. \033[m")

def anularUltimaOperacion(): 
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    imagenResultado = imagenPreviaALaUltimaOperacion.copy()
    
def verResultadosHastaAhora():
    global imagenOriginal
    global imagenPreviaALaUltimaOperacion
    global imagenResultado
    print ("\033[31m Se están mostrando las imágenes, debe cerrarlas para continuar la ejecución.\n \033[m")
    cv2.imshow('ORIGINAL', imagenOriginal)
    cv2.imshow('Imagen previa a la ultima operacion', imagenPreviaALaUltimaOperacion)
    cv2.imshow('RESULTADO', imagenResultado)
    cv2.waitKey()
    cv2.destroyAllWindows()

def salir():
    print ("\033[31m Cerrando aplicación... \033[m")

def imprimirOpcionNoValida():
    print ("\033[31m Opción no válida\n \033[m")

def ejecutarOperacion(numeroOperacion):
        opciones={
                "1":filtroMediana,
                "2":filtroColorRGB,
                "3":fltroBlancoYNegro,
                "4":suavizadoBordes,
                "5":erosionar,
                "6":dilatar,
                "7":guardarImagenEsqueleto,
                "8":recuperarImagenEsqueleto,
                "9":anularUltimaOperacion,
                "10":verResultadosHastaAhora,
                "11":salir,
                }
        funcionAEjecutar=opciones.get(numeroOperacion, imprimirOpcionNoValida)
        return funcionAEjecutar()

rutaImagen = input('Introduce la ruta absoluta de la imagen a analizar:')    
assert os.path.exists(rutaImagen), "No se ha encontrado ningún fichero en la ruta , " + str(rutaImagen)
imagenOriginal = cv2.imread(rutaImagen,1)
imagenPreviaALaUltimaOperacion = imagenOriginal.copy()
imagenResultado = imagenOriginal.copy()
imagenEsqueleto = imagenResultado.copy()
respuestaUsuario = ""
while (respuestaUsuario != "11"):
    print("¿Qué operación desea realizar?\n"
          "1- Aplicar filtro de mediana (Elimina ruido 'Sal y Pimienta').\n"
          "2- Aplicar filtro RGB (Elimina pixeles del color RGB que se le pase como parámetro.).\n"
          "3- Aplicar filtro Blanco/Negro (Elimina cualquier tonalidad de gris).\n"
          "4- Suavizar bordes.\n"
          "5- Erosionar.\n"
          "6- Dilatar.\n"
          "7- Guardar esqueleto de la imagen actual\n"
          "8- Recomponer imagen a partir del esqueleto guardado.\n"
          "9- Anular última operación.\n"
          "10- Ver resultados hasta ahora.\n"
          "11- Salir.")
    respuestaUsuario = input("Selecciona una de las opciones:")
    ejecutarOperacion(respuestaUsuario)
    

