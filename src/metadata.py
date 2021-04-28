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

os.system("cls")

descripion = "Example: -l www.google.com"
parser = argparse.ArgumentParser(description='Metadata', epilog=descripion, formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument("-l,", metavar='--Link', dest="link", help="Link para descargar imagenes", required=True)

params = parser.parse_args()

print("[INFO] Buscando...", params.link)

