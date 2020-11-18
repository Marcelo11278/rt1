''' SE IMPORTAN LAS LIBRERIAS NECESARIAS 
PARA LA EJECUCION DE LAS FUNCIONES'''
import requests
import subprocess
import pdb
import argparse
import warnings
import sys
import os
import socket
from subprocess import call, PIPE
from getmac import get_mac_address

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
        print("Sin conexión a internet")
        return False

def macBD(archivo,mac):
    '''OBTIENE EL FABRICANTE DE LA MAC SEGUN 
       BASE DE DATOS(MANUF.TXT O BD.TXT[DESCARGADA])
    '''
    companiaB = ""
    companiaR = ""
    macU = mac[:8]
    linea = archivo.readline()
    while linea:
        nuevo = linea.split()
        if "/" in nuevo:
            macU = mac
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
    print(f"Vendedor    : {companiaR}")
    
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
        subprocess.run("ping "+ ip, shell=True, check=True, stdout=PIPE)
        macDef = obtener_MAC(ip)
        macBD(archivo, macDef)
    except:
        print("Error: ip is outside the host network")
    


def parametro(archivo):
    '''
       -UNION DE LAS DEMAS FUNCIONES
       -GENERA LA OPCIONES POR INGRESO POR CONSOLA
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip")
    parser.add_argument("--mac")
    args = parser.parse_args()

    ip = args.ip
    mac = args.mac
    try:
        if(mac):
            macBD(archivo,mac)
        elif(ip):
            IpVerificadorMac(archivo, ip)
        else:
            print("Error: OUILookup --ip <IP> | --mac <Mac>")
    except:
        print("***ERROR EN LA EJECUCION DEL SCRIPT***")
    finally:
        archivo.close()
