'''
  IMPORTA LAS FUNCIONES A UTILIZAR
'''
from funciones import descargarBD, main
import sys
'''
  INICIO DEL PROCESO DE RESCATAR ARCHIVO
  - PRIMERO VERIFICA SI HAY CONEXION A INTERNET PARA DESCARGAR LA BD MAS ACTUALIZADA
  - EN CASO CONTRARIO UTILIZA EL ARCHIVO "manuf.txt"
  - LA FUNCION "main(archivo)" ES LA QUE EJECUTA LA LOGICA DEL PROGRAMA
'''
archivo = None
if descargarBD():
  archivo = open("BD.txt","r",encoding='utf-8')
else:
  try:
    archivo = open("manuf.txt", "r",encoding='utf-8')    
  except:
    print("ERROR: El respaldo de la BD no se encuentra")
    exit(1)

main(archivo)


