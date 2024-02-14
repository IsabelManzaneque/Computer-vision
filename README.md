# VA

Proyectos en los que se practican algunos de los conceptos básicos de la administración y el diseño de sistemas operativos haciendo uso del lenguaje C y el lenguaje de script Bash, usando como plataforma el sistema operativo Linux.


## Proyectos

* [Calibracion de la camara](#calibracion-de-la-camara)
* [Descriptores de puntos caracteristicos](#descriptores-de-puntos-caracteristicos)
* [Eliminacion de ruido](#Eliminacion-de-ruido)
* [Reconocimiento de objetos](#Reconocimiento-de-objetos)
* [Segmentacion con conocimiento del dominio](#Segmentacion-con-conocimiento-del-dominio)
* [Segmentacion sin conocimiento del dominio](#Segmentacion-sin-conocimiento-del-dominio)
* [Transformaciones geometricas](#Transformaciones-geometricas)

## Calibracion de la camara

https://github.com/IsabelManzaneque/PEC1_VA/tree/main/Calibracion%20de%20la%20camara

Se sigue el tutorial de la documentación oficial de opencv (https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html) para realizar la calibración de la cámara de un smartphone utilizando un set propio de imágenes de un tablero.

## Descriptores de puntos caracteristicos

https://github.com/IsabelManzaneque/PEC1_VA/tree/main/Descriptores%20de%20puntos%20caracteristicos

## Eliminacion de ruido

https://github.com/IsabelManzaneque/PEC1_VA/tree/main/Eliminacion%20de%20ruido

Aplicación sencilla que permite al usuario especificar una imagen de la que se desea eliminar el ruido y aplicar distintos operadores de manera secuencial. Los operadores disponibles son: 

 - Filtro Non-Local-Means: Elimina el ruido impulsivo utilizando la función “fastNlMeansDenoising”. Esta función implementa un algoritmo de eliminación del ruido basado en un método de filtrado no local y adaptativo: en lugar de calcular el valor de un píxel basándose solo en sus píxeles vecinos, se consideran regiones similares en toda la imagen. Este enfoque es más efectivo para preservar los bordes y las estructuras en la imagen mientras se elimina el ruido.
 - Filtro Mediana: Elimina el ruido impulsivo aplicando la función “medianBlur”. Esta función sustituye el valor de cada píxel en la imagen por la mediana de los valores de los píxeles vecinos en una ventana definida. A diferencia del filtro anterior, este es un método de suavizado local y no es tan efectivo para preservar los bordes y estructuras de la imagen.
 - Filtro Umbralización: Elimina el ruido en tonalidades de gris aplicando la función “threshold”. Convierte una imagen en escala de grises a una imagen binaria: los píxeles
se clasifican como blanco si el valor de su intensidad está por encima del umbral y como negro si está por debajo.
- Filtro negro: Este filtro compara los píxeles de la imagen con un valor umbral. Si la intensidad del pixel es menor a la del valor umbral, establece el pixel a blanco. Útil para eliminar detalles aislados e indeseados de la imagen.
- Realzar bordes: Utiliza la función “filter2D” para realzar los bordes de una imagen aplicando una operación de convolución y un kernel predefinido de refinado de realce de bordes.
- Erosionar: Utiliza la función “dilate” para dilatar el fondo y así erosionar los contornos de los dibujos, reduciendo el grosor de sus bordes.
- Dilatar: Utiliza la función “erode” para erosionar el fondo y así dilatar los contornos de los dibujos, aumentando el grosor de sus bordes.
- Seleccionar ROI: Cualquiera de las anteriores funciones puede utilizarse sobre la imagen al completo o sobre una región de interés. Esta opción permite al usuario seleccionar una región sobre la que aplicar alguno de los operadores, sin que el resto de la imagen se vea afectada.
- Mostrar resultado: Muestra 3 imágenes: La imagen original, la imagen modificada y una comparación AntesDespués de los cambios realizados.
- Restablecer: Restablece la imagen original, eliminando todos los cambios realizados.

Ejemplo de utilización:
![image](https://github.com/IsabelManzaneque/PEC1_VA/assets/86284395/cce604f3-d0ce-452f-97dc-94fe22909b18)




## Reconocimiento de objetos

https://github.com/IsabelManzaneque/PEC1_VA/tree/main/Reconocimiento%20de%20objetos

## Segmentacion con conocimiento del dominio

https://github.com/IsabelManzaneque/PEC1_VA/tree/main/Segmentacion%20con%20conocimiento%20del%20dominio

## Segmentacion sin conocimiento del dominio

https://github.com/IsabelManzaneque/PEC1_VA/tree/main/Segmentacion%20sin%20conocimiento%20del%20dominio

## Transformaciones geometricas

https://github.com/IsabelManzaneque/PEC1_VA/tree/main/Transformaciones%20geometricas

Aplicación sencilla que permite al usuario aplicar distintas transformaciones geométricas a una imagen. Las opciones disponibles son: 

- Reescalar y rotar: Aplica a la imagen parámetro un reescalado de 200 x 200 pixels, una rotacion de 45 grados alrededor del su centro y un reescalado 1:0.7
- Transformacion afin compuesta 1:  Implementa las siguientes transformaciones por separado (con matrices de transformación distintas): Inclinar 30 grados a la derecha la imagen de entrada , girar 90 grados a la izquierda con centro de giro en el centro de la img, reescalar a la mitad en ambos ejes la imagen obtenida de T2. 
- Transformacion afin compuesta 2: Implementa las anteriores transformaciones en un solo paso (con una sola matriz de transformacioón)
- Transformacion polar: obtiene una imagen logPolar cuadrada, centrada en el centro de la imagen original con una fila por grado y ajustada para ver toda la imagen original. 
- Deshacer transformacion polar: Deshace una transformación polar aplicada a una imagen realizando la transformación inversa
- Transformacion no lineal:  Deforma la imagen de manera que su mitad izquierda ocupa 1/3 de la imagen final y la mitad derecha ocupa los 2/3 restantes. 
- Llevar rectangulo a objetivo: Genera una imagen sintetica de un rectangulo de lado 40 x 20 sobre un fondo y realiza una secuencia de transformaciones para colocarlo en una posicion objetivo 

