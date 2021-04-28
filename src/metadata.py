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
    parsed_body = html.fromstring(response.text)

    print(datetime.now(), "\033[0;32m [INFO] Expresion regular para obtener las imagenes //img/@src  \033[0;0m")    
    images = parsed_body.xpath('//img/@src')
    
    print(datetime.now(), "\033[0;32m [INFO] %s imagenes encontradas  \033[0;0m" % len(images))
        
    print(datetime.now(), "\033[0;32m [INFO] Creando carpeta para guardar las imagenes  \033[0;0m")
    os.system("mkdir images")

    print(datetime.now(), "\033[0;32m [INFO] Nueva carpeta llamada images \033[0;0m")
    
    for image in images:
        if image.startswith("http") == False:
            descargar = url + image
        else:
            descargar = image        
        print(datetime.now(), "\033[0;33m [INFO] Descargando imagen... \033[0;0m")
        r = requests.get(descargar)
        f = open('images/%s' % descargar.split('/')[-1], 'wb')
        f.write(r.content)
        f.close()
except Exception as error:    
    print(datetime.now(), "\033[0;91m [ERROR] Ha ocurrido un error en %s" % url)
    print(error)

