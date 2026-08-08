# Proyecto Final - MeteoCaracas

# Descripción General

MeteoCaracas es un sistema que desarrollamos en Python usando Programación Orientada a Objetos (POO) para consultar el clima en tiempo real y analizar datos históricos en las distintas zonas del Área Metropolitana de Caracas (Municipios Baruta, Chacao, El Hatillo, Libertador y Sucre). 

Para iniciar, el programa lee el archivo zonas_caracas.json, convirtiendo toda la información en objetos de las clases Municipio y Localidad, mostrando un reporte sobre cuántas zonas tienen coordenadas y cuántas no. Luego, se conecta a la API de Open-Meteo para buscar el clima de cualquier localidad. Además, la aplicación guarda las estadísticas de las consultas hechas durante la sesión y permite revisar históricos de clima con gráficos para comparar cómo ha cambiado el tiempo entre varios años.

# Integrantes del Equipo

Anthony Fakhri — C.I.: 31.415.437

Manuela Machado — C.I.: 31.312.345

# Funcionalidades del Sistema

**1. Carga de Datos y Diagnóstico Inicial:** Al iniciar, el sistema lee la base de datos geográfica y genera un reporte detallado indicando por cada municipio el total de localidades, la cantidad con coordenadas conocidas, la cantidad sin coordenadas y el porcentaje de cobertura disponible.

**2. Consulta de Clima en Tiempo Real:** Muestra en pantalla el municipio, localidad, coordenadas, temperatura actual en °C, humedad relativa en %, velocidad del viento en km/h y el estado o código del tiempo.

**3. Reportes y Estadísticas:** Mantiene un ranking con las localidades más cálidas y más frías, el cálculo de la temperatura promedio general de las zonas consultadas durante la sesión y el reporte de cobertura geográfica agrupado por municipios para localidades sin coordenadas registradas.

**4. Históricos y Visualización Gráfica:** Permite seleccionar un rango de fechas en formato AAAA-MM-DD para evaluar una localidad con coordenadas válidas. Muestra datos mensuales y promedios de temperatura, humedad, precipitación acumulada y velocidad del viento, identifica los años más calurosos, frescos, húmedos y lluviosos, y genera gráficos comparativos sobre la evolución.
