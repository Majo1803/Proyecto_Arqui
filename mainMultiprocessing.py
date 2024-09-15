#Importaciones de bibliotecas
from ast import Global
import glob
from tkinter.tix import IMAGE
from PIL import Image
from scipy import spatial
import numpy as np
import sys
import time
from multiprocessing import Pool






#Define ruta de imagenes para el collage, la imagen base y su tamaño
def buscarRuta():

	global inicioApp,rutaCarpetaImagenes,rutaImagenPrincipal,tamañoMosaico

	inicioApp = time.time() #Comienza a medir el tiempo del proceso

	inicioBuscarRuta= time.time() #Comienza a medir el tiempo del proceso
	rutaImagenPrincipal= "gato.jpg"   #---> imagen que se pixeliará / cambiar ruta para hacer diferentes pruebas
	rutaCarpetaImagenes="prueba\\*"  #---->imagenes que la formaran
	tamañoMosaico=(25,25) #---->tamaño de las imagenes que formaran el collage
	finalBuscarRuta= time.time()


	print("\nEl tiempo de ejecucion para buscar las rutas de las imagenes es de  %f segundos\n"% (finalBuscarRuta - inicioBuscarRuta))


#Obtener todas las imagenes de la carpeta
def obtenerImagen():

	#global imagenesCollage

	inicioObtenerImage = time.time() #Comienza a medir el tiempo del proceso
	imagenesCollage=[] #------> lista donde se almacenan las imagenes para el collage
	for imagen in glob.glob(rutaCarpetaImagenes): #--->por cada imagen dentro de la carpeta Prueba
		imagenesCollage.append(imagen) #-----> se agrega la imagen a la lista
	finalObtenerImage = time.time() #Comienza a medir el tiempo del proceso

	print("\nEl tiempo de ejecucion para obtener las imagenes del collage es de  %f segundos\n"% (finalObtenerImage - inicioObtenerImage))
	return imagenesCollage

#Modificar el tamaño de las imagenes guardadas para utilizarlas en el collage
def modificarTamano(imagenesCollage):
	#global imagenesListas

	inicioModificarImage = time.time() #Comienza a medir el tiempo del proceso
	imagenesListas=[]#------->lista de imagenes listas para armar el collage
	for x in imagenesCollage: #------>por cada elemento dentro de la lista de imagenes
		imagenObtenida=Image.open(x) #----------> se abre
		imagenObtenida=imagenObtenida.resize(tamañoMosaico) #------->se redimenciona según lo definido
		imagenesListas.append(imagenObtenida)#--------> se guarda en la lista de imagenes listas para utilizarce
	finalModificarImage = time.time() #Comienza a medir el tiempo del proceso

	print("\nEl tiempo de ejecucion para modificar el tamaño de las imagenes es de %f segundos\n"% (finalModificarImage-inicioModificarImage))
	return imagenesListas


#Colores promedios e inserción en arrays según valor RGB
def colorPromedio(imagenesListas):

	#global coloresPixeles

	inicioColoresPromd= time.time() #Comienza a medir el tiempo del proceso
	coloresPixeles=[]#--->almacena las imagenes según color
	for imagenObtenida in imagenesListas:
		color_promedio=np.array(imagenObtenida).mean(axis=0).mean(axis=0)#-->obtiene el valor RGB
		coloresPixeles.append(color_promedio)#------->almacena
	finalColoresPromd = time.time() #Comienza a medir el tiempo del proceso

	print("\nEl tiempo de ejecucion para obtener los colores promedios de las imagenes es de %f segundos\n"% (finalColoresPromd-inicioColoresPromd))

	return coloresPixeles

#Cambiar tamaño imagen base para pixelearla
def cambioTamanoBase():
	global redimensionBase,altura,ancho,imagenBase

	inicioCambioTamano= time.time() #Comienza a medir el tiempo del proceso
	imagenBase=Image.open(rutaImagenPrincipal) #------->abre la imagen base
	ancho= int(np.round(imagenBase.size[0]/tamañoMosaico[0])) #----->divide el ancho de la imagen base entre el tamaño de las imagenes para formarla
	altura=int(np.round(imagenBase.size[1]/tamañoMosaico[1]))#-----> divide el alto de la imagen base entre el tamaño de las imagenes para formarla
	redimensionBase=imagenBase.resize((ancho,altura))#------>redimenciona la imagen
	finalCambioTamano = time.time() #Comienza a medir el tiempo del proceso


	print("\nEl tiempo de ejecucion para cambiar el tamaño de la imagen base del collage es de %f segundos\n"% (finalCambioTamano-inicioCambioTamano))


#Encontrar imagen para pixel color
def imagenPorPixel(coloresPixeles):
	#global imagenColor

	inicioEncontarPixel = time.time() #Comienza a medir el tiempo del proceso
	tree=spatial.KDTree(coloresPixeles)
	imagenColor=np.zeros((ancho,altura),dtype=np.uint32)
	for i in range(ancho):
		for j in range(altura):
			closet=tree.query(redimensionBase.getpixel((i,j)))
			imagenColor[i,j]=closet[1]
	finalEncontarPixel = time.time() #Comienza a medir el tiempo del proceso

	print("\nEl tiempo de ejecucion para encontrar las imagenes que coincide con cada de pixel la imagen base es de %f segundos\n"% (finalEncontarPixel-inicioEncontarPixel))

	return imagenColor

#Empieza a formar la imagen final a partir de las imagenes 
def crearCollage(imagenColor,imagenesListas):


	inicioNuevaImage = time.time() #Comienza a medir el tiempo del proceso
	imagenFinal = Image.new('RGB', imagenBase.size) #Compara el RGB con la imagen base cuadriculada para crear una nueva
	for i in range(ancho):#--->i es fila
		for j in range(altura):#--->j es columna
			# Posición
			x, y = i*tamañoMosaico[0], j*tamañoMosaico[1]
			# Cambio a imagen
			index = imagenColor[i, j]
			# Salida para formar la imagen final
			imagenFinal.paste(imagenesListas[index], (x, y))
	imagenFinal.save("final.jpg",quality=100)#----->salva la imagen final

	finalNuevaImage = time.time() #Comienza a medir el tiempo del proceso
	print("\nEl tiempo de ejecucion para ensamblar la nueva imagen es de %f segundos\n"% (finalNuevaImage-inicioNuevaImage))

#Impresión de imagen final en pantalla
def mostrarCollage():

	inicioShowImage = time.time() #Comienza a medir el tiempo del proceso
	im=Image.open("final.jpg")
	im.show()
	finalShowImage = time.time() #Comienza a medir el tiempo del proceso
	print("\nEl tiempo de ejecucion para mostrar la nueva imagen es de %f segundos\n"% (finalShowImage-inicioShowImage))



if __name__ == '__main__':
	
	"""
	#intento de multiprocesamiento
	buscarRuta()
	imagenesCollage=obtenerImagen()
	with Pool(4) as p:
		imagenesListas=p.map(modificarTamano,imagenesCollage)
		print(imagenesListas)

		coloresPixeles=p.map(colorPromedio,imagenesListas)
		print(coloresPixeles)

	cambioTamanoBase()
	with Pool(4) as p:
		imagenColor=p.map(imagenPorPixel,coloresPixeles)
		print(imagenColor)
	crearCollage(imagenColor,imagenesListas)
	mostrarCollage()
	"""
	
	buscarRuta()
	imagenesCollage=obtenerImagen()
	imagenesListas=modificarTamano(imagenesCollage)
	coloresPixeles=colorPromedio(imagenesListas)
	cambioTamanoBase()
	imagenColor=imagenPorPixel(coloresPixeles)
	crearCollage(imagenColor,imagenesListas)
	mostrarCollage()


	finalApp = time.time()
	print("\nEl tiempo TOTAL de ejecucion para creacion del collage ha sido de %f segundos\n"% (finalApp - inicioApp))
