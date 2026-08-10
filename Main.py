"""
En este archivo gestionamos el programa principal y menú interactivo:
1. Cargar la información inicial de los municipios y localidades.
2. Permitir la consulta de clima por navegación de municipio o por búsqueda directa.
3. Mostrar las estadísticas y reportes acumulados durante la sesión.
4. Generar análisis históricos y gráficos meteorológicos comparativos.
"""

from Modelos import Municipio, Localidad
from App import GestorDatos
from Servicios import ServicioApiClima
from Estadisticas import GestorEstadisticas, GestorHistorico

def buscar_localidades_por_nombre(municipios: list[Municipio], texto_busqueda: str) -> list[tuple[Municipio, Localidad]]:
    # Busca coincidencias parciales del nombre de la localidad en todos los municipios.
    coincidencias = []
    texto_lower = texto_busqueda.lower().strip()
    for mun in municipios:
        for loc in mun.localidades:
            if texto_lower in loc.nombre.lower() and loc.tiene_coordenadas():
                coincidencias.append((mun, loc))
    return coincidencias

def ejecutar_menu_principal() -> None:
    # Función principal que controla la ejecución de MeteoCaracas.
    gestor_datos = GestorDatos()
    municipios = gestor_datos.cargar_municipios_desde_json("zonas_caracas.json")

    if not municipios:
        print("\nNo se pudieron cargar los datos iniciales. Finalizando programa.")
        return

    # Muestra el reporte de carga requerido al iniciar
    gestor_datos.mostrar_reporte_carga(municipios)
    gestor_stats = GestorEstadisticas()
    gestor_historico = GestorHistorico()

    while True:
        print("MENÚ PRINCIPAL METEOCARACAS")
        print("1. Consulta del clima en tiempo real (Por Municipio y Localidad)")
        print("2. Consulta del clima en tiempo real (Búsqueda directa por nombre)")
        print("3. Módulo de Reportes y Estadísticas de Sesión")
        print("4. Módulo Histórico y Gráficos Comparativos")
        print("5. Salir del programa")

        opcion = input("\nSeleccione una opción (1-5): ").strip()

        if opcion == "1":
            print("\n--- SELECCIÓN DE MUNICIPIO ---")
            for i, mun in enumerate(municipios, 1):
                print(f"{i}. {mun.nombre}")

             try:
                idx_m = int(input("\nElija el número del municipio: ")) - 1
                if 0 <= idx_m < len(municipios):
                    mun_sel = municipios[idx_m]
                    locs_validas = mun_sel.obtener_localidades_con_coordenadas()

                    if not locs_validas:
                        print(f"\nEl municipio {mun_sel.nombre} no posee localidades con coordenadas válidas.")
                        continue

                    print(f"\nLOCALIDADES DISPONIBLES EN {mun_sel.nombre.upper()}")
                    for j, loc in enumerate(locs_validas, 1):
                        print(f"{j}. {loc.nombre}")

                    idx_l = int(input("\nElija el número de la localidad: ")) - 1
                    if 0 <= idx_l < len(locs_validas):
                        loc_sel = locs_validas[idx_l]
                        reg = ServicioApiClima.consultar_clima_actual(
                            mun_sel.nombre, loc_sel.nombre, loc_sel.latitud, loc_sel.longitud
                        )
                        if reg:
                            reg.mostrar_detalle()
                            gestor_stats.registrar_consulta(reg)
                    else:
                        print("\nSelección de localidad fuera de rango.")