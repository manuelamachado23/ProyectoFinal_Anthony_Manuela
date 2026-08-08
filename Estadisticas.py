"""
En este archivo gestionamos los análisis y métricas del sistema:
1. Calcular el ranking de temperaturas (más cálida y más fría) en la sesión.
2. Generar el reporte de cobertura geográfica para zonas sin coordenadas.
3. Calcular el promedio general de temperaturas de las consultas activas.
4. Consultar datos históricos en Open-Meteo y graficar con Pandas y Matplotlib.
"""

import matplotlib.pyplot as plt
import pandas as pd
import requests
from Modelos import Municipio, RegistroClima

class GestorEstadisticas:
   # Clase para procesar reportes en memoria.

   def __init__(self):
       self.consultas_sesion: list[RegistroClima] = []

   def registrar_consulta(self, registro: RegistroClima) -> None:
       self.consultas_sesion.append(registro)

   def ranking_temperatura(self) -> None:
       # Muestra la localidad más cálida y más fría consultada en la sesión activa.
       if not self.consultas_sesion:
           print("\nAún no se han realizado consultas de clima en esta sesión.")
           return

       mas_calida = max(self.consultas_sesion, key=lambda x: x.temperatura)
       mas_fria = min(self.consultas_sesion, key=lambda x: x.temperatura)
       
       print("\nRANKING DE TEMPERATURA")
       print()
       print(f"  Más cálida: {mas_calida.localidad} ({mas_calida.municipio}) -> {mas_calida.temperatura} °C")
       print(f"  Más fría:   {mas_fria.localidad} ({mas_fria.municipio}) -> {mas_fria.temperatura} °C")

   def reporte_cobertura_geografica(self, municipios: list[Municipio]) -> None:
       # Localidades sin coordenadas registradas agrupadas por municipio.
       print("\nCOBERTURA GEOGRÁFICA (LOCALIDADES SIN COORDENADAS)")
       for mun in municipios:
           sin_coords = mun.obtener_localidades_sin_coordenadas()
           print(f"\nMunicipio: {mun.nombre} ({len(sin_coords)} sin coordenadas)")
           if not sin_coords:
               print("  (Todas las localidades tienen coordenadas registradas)")
           else:
               for loc in sin_coords:
                   print(f"  - {loc.nombre}")

   def promedio_general_temperatura(self) -> None:
       # Calcula e informa el promedio general de temperaturas consultadas en la sesión."""
       if not self.consultas_sesion:
           print("\nNo hay datos suficientes para calcular el promedio de la sesión.")
           return

       total_temp = sum(reg.temperatura for reg in self.consultas_sesion)
       promedio = total_temp / len(self.consultas_sesion)
       print(f"\nPROMEDIO GENERAL DE LA SESIÓN")
       print(f"Promedio de temperatura ({len(self.consultas_sesion)} consultas): {promedio:.2f} °C")

class GestorHistorico:
   # Módulo para consultar datos históricos y generar gráficos comparativos.

   def consultar_y_graficar_historico(
       self, latitud: float, longitud: float, nombre_localidad: str, fecha_inicio: str, fecha_fin: str
   ) -> None:
       # Obtiene datos históricos diarios de Open-Meteo, procesa con pandas y grafica con matplotlib.
       url = "https://archive-api.open-meteo.com/v1/archive"
       params = {
           "latitude": latitud,
           "longitude": longitud,
           "start_date": fecha_inicio,
           "end_date": fecha_fin,
           "daily": [
               "temperature_2m_mean",
               "relative_humidity_2m_mean",
               "precipitation_sum",
               "wind_speed_10m_max"
           ],
           "timezone": "auto"
       }
