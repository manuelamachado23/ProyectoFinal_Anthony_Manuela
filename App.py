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

           for nombre_municipio, lista_locs in datos_raw.items():
               municipio_obj = Municipio(nombre=nombre_municipio)
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
           print(f"\n No se encontró el archivo '{ruta_archivo}'. Verifique la ruta.")
       except json.JSONDecodeError:
           print(f"\n El archivo '{ruta_archivo}' contiene un formato JSON inválido.")
       except Exception as e:
           print(f"\n Error al cargar los datos: {e}")

       return lista_municipios

   def mostrar_reporte_carga(self, municipios: list[Municipio]) -> None:
       # Genera un reporte en pantalla indicando las métricas requeridas por cada municipio.
       print("REPORTE DE CARGA DE DATOS INICIAL")
       for mun in municipios:
           total = mun.obtener_total_localidades()
           con_coords = len(mun.obtener_localidades_con_coordenadas())
           sin_coords = len(mun.obtener_localidades_sin_coordenadas())
           porcentaje = mun.calcular_porcentaje_coordenadas()

           print(f"\nMunicipio: {mun.nombre}")
           print(f"  a. Cantidad total de localidades: {total}")
           print(f"  b. Localidades con coordenadas:   {con_coords}")
           print(f"  c. Localidades sin coordenadas:   {sin_coords}")
           print(f"  d. Porcentaje con coordenadas:   {porcentaje:.2f}%")