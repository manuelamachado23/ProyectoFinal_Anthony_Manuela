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
       # Calcula e informa el promedio general de temperaturas consultadas en la sesión.
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

        try: 
           resp = requests.get(url, params=params, timeout=15)
           resp.raise_for_status()
           data = resp.json()
           daily_data = data.get("daily", {})

           if not daily_data or "time" not in daily_data:
               print("No se obtuvieron registros para el rango especificado.")
               return

           df = pd.DataFrame({
               "Fecha": pd.to_datetime(daily_data["time"]),
               "Temperatura": daily_data["temperature_2m_mean"],
               "Humedad": daily_data["relative_humidity_2m_mean"],
               "Precipitacion": daily_data["precipitation_sum"],
               "Viento": daily_data["wind_speed_10m_max"]
           })

           df["Año"] = df["Fecha"].dt.year

           print(f"\nPROMEDIOS HISTÓRICOS ({nombre_localidad})")
           print(f"• Temperatura Promedio: {df['Temperatura'].mean():.2f} °C")
           print(f"• Humedad Promedio:     {df['Humedad'].mean():.2f} %")
           print(f"• Precipitación Total:  {df['Precipitacion'].sum():.2f} mm")
           print(f"• Viento Máx Promedio:  {df['Viento'].mean():.2f} km/h")

           agrupado_año = df.groupby("Año").agg({
               "Temperatura": "mean",
               "Humedad": "mean",
               "Precipitacion": "sum"
           })

           if not agrupado_año.empty:
               año_caluroso = agrupado_año["Temperatura"].idxmax()
               año_fresco = agrupado_año["Temperatura"].idxmin()
               año_lluvioso = agrupado_año["Precipitacion"].idxmax()
               año_humedo = agrupado_año["Humedad"].idxmax()
               print(f"\nANÁLISIS COMPARATIVO POR AÑO")
               print(f"  Año más caluroso:      {año_caluroso}")
               print(f"  Año más fresco:        {año_fresco}")
               print(f"  Año más lluvioso:      {año_lluvioso}")
               print(f"  Año con mayor humedad: {año_humedo}")

           plt.figure(figsize=(10, 6))
           plt.plot(df["Fecha"], df["Temperatura"], label="Temperatura (°C)", color="tab:red")
           plt.plot(df["Fecha"], df["Humedad"], label="Humedad (%)", color="tab:blue")
           plt.plot(df["Fecha"], df["Viento"], label="Viento (km/h)", color="tab:green")
           plt.title(f"Evolución Meteorológica - {nombre_localidad} ({fecha_inicio} a {fecha_fin})")
           plt.xlabel("Fecha")
           plt.ylabel("Magnitudes")
           plt.legend()
           plt.grid(True)
           plt.tight_layout()
           plt.show()

       except requests.exceptions.RequestException as e:
           print(f"Ocurrió un error al consultar el histórico: {e}")
       except Exception as e:
           print(f"ERROR {e}")