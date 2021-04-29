"""
Uso: Metadata de imagenes en la web
Creador: Andrés Hernández Mata
Version: 1.0.0
Python: 3.9.1
Fecha: 26 Abril 2020
"""

import argparse
import os
from datetime import datetime
import requests
from lxml import html
from bs4 import BeautifulSoup
import pathlib
from PIL import Image
from PIL.ExifTags import TAGS

os.system("cls")

def main():
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
            req = requests.get(descargar)
            imagen = descargar.split('/')[-1]
            file_imagen = open('images/%s' % imagen, 'wb')
            print(datetime.now(), "\033[0;33m [INFO] Descargando %s\033[0;0m" % imagen)
            file_imagen.write(req.content)
            file_imagen.close()
            print_metadata(imagen)        
        print(datetime.now(), "\033[0;32m [INFO] Success \033[0;0m")
    except Exception as error:
        print(datetime.now(), "\033[0;91m [ERROR] Ha ocurrido un error en %s" % url)
        print(error)

def decode_gps_info(exif):
    gpsinfo = {}
    if 'GPSInfo' in exif:
        #Parse geo references.
        Nsec = exif['GPSInfo'][2][2] 
        Nmin = exif['GPSInfo'][2][1]
        Ndeg = exif['GPSInfo'][2][0]
        Wsec = exif['GPSInfo'][4][2]
        Wmin = exif['GPSInfo'][4][1]
        Wdeg = exif['GPSInfo'][4][0]
        if exif['GPSInfo'][1] == 'N':
            Nmult = 1
        else:
            Nmult = -1
        if exif['GPSInfo'][3] == 'E':
            Wmult = 1
        else:
            Wmult = -1
        Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
        Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)
        exif['GPSInfo'] = {"Lat" : Lat, "Lng" : Lng}

def get_metadata(image_path):
    ret = {}
    image = Image.open(image_path)
    if hasattr(image, '_getexif'):
        exifinfo = image._getexif()
        if exifinfo is not None:
            for tag, value in exifinfo.items():
                decoded = TAGS.get(tag, tag)
                ret[decoded] = value
    decode_gps_info(ret)
    return ret

def print_metadata(imagen):
    file = open("metadata/%s%s" % (imagen.split(".")[-2], ".txt"), 'w')    
    file.write("[+] Metadata for file: %s " %(imagen))
    file.write(os.linesep)
    try:
        exifData = {}
        exif = get_metadata("images/%s" % imagen)
        for metadata in exif:
            file.write("Metadata: %s - Value: %s " %(metadata, exif[metadata]))
            file.write(os.linesep)
    except:
        import sys, traceback
        traceback.print_exc(file=sys.stdout)
    file.close()
    print(datetime.now(), "\033[0;32m [INFO] Obteniendo la metadata de %s\033[0;0m" % imagen)

if __name__ == '__main__':
    main()



