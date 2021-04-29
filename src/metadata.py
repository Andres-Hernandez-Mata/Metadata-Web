"""
Uso: Metadata de imagenes en la web
Creador: Andrés Hernández Mata
Version: 1.0.0
Python: 3.9.1
Fecha: 26 Abril 2020
"""

import argparse
import os
import time
from datetime import datetime
import time
import requests
from lxml import html
from bs4 import BeautifulSoup
import pathlib

os.system("cls")

descripion = "Example: -l https://www.google.com.mx"
parser = argparse.ArgumentParser(description='Metadata', epilog=descripion, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-l,", metavar='--Link', dest="link", help="Link para descargar imagenes", required=True)

params = parser.parse_args()
url = params.link

print(datetime.now(), "\033[0;32m [INFO] Buscando... %s \033[0;0m" % url)
print(datetime.now(), "\033[0;32m [INFO] Obteniendo imagenes de... %s \033[0;0m" % url)

try:    
    response = requests.get(url)  
    bs = BeautifulSoup(response.text, 'lxml')
    parsed_body = html.fromstring(response.text)

    print(datetime.now(), "\033[0;32m [INFO] Expresion regular para obtener las imagenes //img/@src  \033[0;0m")    
    images = parsed_body.xpath('//img/@src')
    
    print(datetime.now(), "\033[0;32m [INFO] %s imagenes encontradas \033[0;0m" % len(images))            
    
    carpeta_images = pathlib.Path("images")
    if carpeta_images.exists():
        print(datetime.now(), "\033[0;32m [INFO] Almacenando las imagenes en la carpeta images \033[0;0m")
    else:
        os.system("mkdir images")
        print(datetime.now(), "\033[0;32m [INFO] Creando carpeta para guardar las imagenes \033[0;0m")
        print(datetime.now(), "\033[0;32m [INFO] Nueva carpeta llamada images \033[0;0m")
    
    carpeta_metadata = pathlib.Path("metadata")
    if carpeta_metadata.exists():
        print(datetime.now(), "\033[0;32m [INFO] Obteniendo la informacion de cada imagen en la carpeta metadata \033[0;0m")
    else:
        os.system("mkdir metadata")
        print(datetime.now(), "\033[0;32m [INFO] Creando carpeta para guardar la metadata de cada imagen  \033[0;0m")
        print(datetime.now(), "\033[0;32m [INFO] Nueva carpeta llamada metadata \033[0;0m")
    
    for tagImage in bs.find_all("img"):
        if tagImage['src'].startswith("http") == False:
            descargar = url + tagImage['src']
        else:
            descargar = tagImage['src']                        
        r = requests.get(descargar)
        imagen = descargar.split('/')[-1]
        f = open('images/%s' % imagen, 'wb')
        print(datetime.now(), "\033[0;33m [INFO] Descargando %s\033[0;0m" % imagen)
        f.write(r.content)
        f.close()
except Exception as error:    
    print(datetime.now(), "\033[0;91m [ERROR] Ha ocurrido un error en %s" % url)
    print(error)
    pass

print(datetime.now(), "\033[0;32m [INFO] Success \033[0;0m")


