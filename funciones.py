''' SE IMPORTAN LAS LIBRERIAS NECESARIAS 
PARA LA EJECUCION DE LAS FUNCIONES'''
import requests
import subprocess
import os
from subprocess import PIPE
from getmac import get_mac_address
import getopt
import sys

def obtener_MAC(host):
    '''RETORMA MAC DEPENDIENDO DE LA IP QUE SE INGRESE'''
    return get_mac_address(ip=host)

def descargarBD():
    '''
        DESCARGA LA BD DE LA PAGINA WEB: https://gitlab.com/wireshark/wireshark/-/raw/master/manuf
    '''
    try:
        url = 'https://gitlab.com/wireshark/wireshark/-/raw/master/manuf'
        myfile = requests.get(url)
        archivo = open('BD.txt', 'wb')
        archivo.write(myfile.content)
        return True
    except:
        print("Sin conexión a internet para descargar BD")
        print("Se usará la de Respaldo\n")
        return False

def macBD(archivo, mac):
    '''
       OBTIENE EL FABRICANTE DE LA MAC SEGUN 
       BASE DE DATOS(MANUF.TXT O BD.TXT[DESCARGADA])
    '''

    companiaB = ""
    companiaR = ""
    macU = (mac[:8]).upper()
    linea = archivo.readline()
    while linea:
        nuevo = linea.split()
        if len(nuevo[2:]) <= 0:
            companiaB = "".join(nuevo[1:2])

        if len(nuevo[2:]) > 0:
            companiaB = " ".join(nuevo[2:])

        if(len(nuevo)) > 0:
      
            if macU.upper() == "".join(nuevo[0]):

                companiaR = companiaB
                break
            else:
                companiaR = "Not Found"

        linea = archivo.readline()

    print(f"MAC address : {mac}")
    print(f"Vendedor    : {companiaR}\n")


def IpVerificadorMac(archivo, ip):
    '''
        DATO QUE EL MODULO SUBPROCESS NOS PERMITE OBTENER LOS DATOS ENVIADOS
        A LA SALIDA EN CONSOLA LO OCUPAMOS PARA VERIFICAR LA SALIDA DEL COMANDO 
        PING HACIA UNA DIRECCION IP, EL CUAL ESTA INICIALIZADO EN TRUE, POR ENDE 
        SI NOS ARROJA UN VALOR DISTINTO DE ESTE SE IRA A LA SECCION EXCEPT, DE LO 
        CONTRARIO, LE PEDIMOS LA MAC QUE CORRESPONDE A ESA IP Y LA VERIFICAMOS 
        EN LA BASE DE DATOS
    '''
    try:
        subprocess.run("ping " + ip, shell=True, check=True, stdout=PIPE)
        macDef = obtener_MAC(ip)
        macBD(archivo, macDef)
    except:
        print("Error: ip is outside the host network")

def main(archivo):
    '''
       -UNION DE LAS DEMAS FUNCIONES
       -GENERA LA OPCIONES POR INGRESO POR CONSOLA POR MEDIO DE GETOPT
    '''
    ip = None
    mac = None
    try:
        options, args = getopt.getopt(sys.argv[1:], "i,m", ['ip=', 'mac=','help'])
    except:
        print("Error: Parametros incorrectos.")
        mensajeError()

    if(options == []):
        print("ERROR: No ingreso parametros")
        mensajeError()

    for opt, arg in options:
        if opt in ('--help'):
            mensajeHelp()
        if opt in ('--ip'):
            ip = arg
        elif opt in ('--mac'):
            mac = arg
    try:
        if(mac):
            macBD(archivo, mac)
        elif(ip):
            IpVerificadorMac(archivo, ip)
    except:
        print("***ERROR EN LA EJECUCION DEL SCRIPT***")
    finally:
        archivo.close()

def mensajeError():
    print("Use: " + sys.argv[0] + " --ip <IP> | --mac <IP> [--help]")
    exit(1)
def mensajeHelp():
    print("Use: " + sys.argv[0] + " --ip <IP> | --mac <IP> [--help]")
    print("      --ip  : specify the IP of the host to query.")
    print("      --mac : specify the MAC address to query.")
    print("      --help: show this message and quit.")
    exit(1)
