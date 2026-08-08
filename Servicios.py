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

   @classmethod
   def mapear_codigo_wmo(cls, codigo: int) -> str:
       # Traduce el número de código meteorológico WMO.
       codigos_wmo = {
           0: "Despejado",
           1: "Principalmente despejado",
           2: "Parcialmente nublado",
           3: "Nublado",
           45: "Niebla",
           48: "Niebla con escarcha",
           51: "Llovizna ligera",
           53: "Llovizna moderada",
           55: "Llovizna densa",
           61: "Lluvia ligera",
           63: "Lluvia moderada",
           65: "Lluvia fuerte",
           80: "Chubascos ligeros",
           81: "Chubascos moderados",
           82: "Chubascos violentos",
           95: "Tormenta eléctrica",
       }
       return codigos_wmo.get(codigo, "Estado desconocido / No registrado")

   @classmethod
   def consultar_clima_actual(
       cls, municipio: str, localidad: str, latitud: float, longitud: float
   ) -> RegistroClima | None:
       # Realiza la solicitud web a Open-Meteo y retorna un objeto RegistroClima.
       parametros = {
           "latitude": latitud,
           "longitude": longitud,
           "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m", "weather_code"]
       }

       try:
           respuesta = requests.get(cls.URL_BASE, params=parametros, timeout=10)
           respuesta.raise_for_status()
           datos_json = respuesta.json()
           datos_current = datos_json.get("current", {})
           temp = datos_current.get("temperature_2m", 0.0)
           hum = int(datos_current.get("relative_humidity_2m", 0))
           vie = datos_current.get("wind_speed_10m", 0.0)
           wmo = datos_current.get("weather_code", 0)
           estado_texto = cls.mapear_codigo_wmo(wmo)

           return RegistroClima(
               municipio=municipio,
               localidad=localidad,
               latitud=latitud,
               longitud=longitud,
               temperatura=temp,
               humedad=hum,
               viento=vie,
               estado_tiempo=estado_texto
           )

       except requests.exceptions.RequestException as error:
           print(f" Error de conexión con la API: {error}")
           return None