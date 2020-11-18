'''
  IMPORTA LIBRERIAS NECESARIAS Y LAS FUNCIONES A UTILIZAR
'''
from os import remove
from funciones import descargarBD, parametro

'''
  INICIO DEL PROCESO DE RESCATAR ARCHIVO
  - GENERA UN ARCHIVO "x.txt" PARA PODER INICIALIZAR VARIABLE
    "archivo" PARA LUEGO TRABAJAR EN SU MANIPULACION
  - PRIMERO VERIFICA SI HAY CONEXION A INTERNET PARA DESCARGAR LA BD MAS ACTUALIZADA
  - EN CASO CONTRARIO UTILIZA EL ARCHIVO "manuf.txt"
  - LA FUNCION "parametro(archivo)" ES LA QUE EJECUTA LA LOGICA DEL PROGRAMA

'''
archivo = open("x.txt","w",encoding='utf-8')
try:
  if descargarBD():
    archivo = open("BD.txt","r",encoding='utf-8')
  else:
    try:
      archivo = open("manuf", "r",encoding='utf-8')
    
    except:
      print("El respaldo de la BD no se encuentra")
except:
  print("No se encuentra la BD de MACs")
  archivo.close()
finally:
  remove("x.txt")

parametro(archivo)


