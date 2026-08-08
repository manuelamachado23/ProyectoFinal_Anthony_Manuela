"""
En este archivo gestionamos los servicios principales del sistema:
1. Cargar el archivo zonas_caracas.json y transformar la data en objetos.
2. Hacer las peticiones a la API meteorológica (Open-Meteo) para traer el clima.
3. Interpretar los códigos meteorológicos WMO a texto legible.
"""

import json
import requests
from Modelos import Municipio, Localidad, RegistroClima

class CargadorDatos:
   # Clase encargada de leer el archivo local y construir los objetos del sistema.

   @classmethod
   def cargar_zonas(cls, ruta_archivo: str = "zonas_caracas.json") -> list[Municipio]:
       # Lee el JSON y convierte los datos en instancias de Municipio y Localidad.
       lista_municipios: list[Municipio] = []

       try:
           with open(ruta_archivo, "r", encoding="utf-8") as archivo:
               datos = json.load(archivo)

           for nombre_mun, lista_locs in datos.items():
               municipio_obj = Municipio(nombre_mun)

               for loc in lista_locs:
                   nombre_zona = loc.get("localidad") or loc.get("nombre") or "Desconocida"

                   localidad_obj = Localidad(
                       nombre=nombre_zona,
                       latitud=loc.get("latitud"),
                       longitud=loc.get("longitud")
                   )
                   municipio_obj.agregar_localidad(localidad_obj)

               lista_municipios.append(municipio_obj)

       except FileNotFoundError:
           print(f"\nNo se encontró el archivo '{ruta_archivo}'.")
       except json.JSONDecodeError:
           print("\nEl archivo JSON tiene un formato inválido.")
       return lista_municipios

class ServicioApiClima:
   # Clase encargada de realizar las peticiones a la API de Open-Meteo.

   URL_BASE: str = "https://api.open-meteo.com/v1/forecast"