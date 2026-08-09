"""
En este archivo gestionamos la carga inicial y el reporte de datos:
1. Leer el archivo JSON para procesar la información de municipios y localidades.
2. Convertir las lecturas del archivo en objetos de las clases Municipio y Localidad.
3. Emitir el reporte detallado de la carga de datos inicial.
"""

import json
from Modelos import Municipio, Localidad

class GestorDatos:
   # Clase encargada del procesamiento de archivos e inicialización del sistema.

   def cargar_municipios_desde_json(self, ruta_archivo: str = "zonas_caracas.json") -> list[Municipio]:
       # Lee el archivo JSON especificado e instancia una lista de objetos Municipio.
       lista_municipios: list[Municipio] = []
       try:
           with open(ruta_archivo, "r", encoding="utf-8") as archivo:
               datos_raw = json.load(archivo)