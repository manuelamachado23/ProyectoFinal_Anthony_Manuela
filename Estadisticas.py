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

