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
        print("\nMENÚ PRINCIPAL METEOCARACAS")
        print("1. Consulta del clima en tiempo real (Por Municipio y Localidad)")
        print("2. Consulta del clima en tiempo real (Búsqueda directa por nombre)")
        print("3. Módulo de Reportes y Estadísticas de Sesión")
        print("4. Módulo Histórico y Gráficos Comparativos")
        print("5. Salir del programa")

        opcion = input("\nSeleccione una opción (1-5): ").strip()

        if opcion == "1":
            print("\nSELECCIÓN DE MUNICIPIO ")
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
                else:
                    print("\nSelección de municipio fuera de rango.")
            except ValueError:
                print("\nIngrese un número entero válido.")

        elif opcion == "2":
            query = input("\nIngrese el nombre (o parte) de la localidad a buscar: ")
            resultados = buscar_localidades_por_nombre(municipios, query)

            if not resultados:
                print("\nNo se encontraron localidades con coordenadas válidas que coincidan con la búsqueda.")
            else:
                print(f"\nCoincidencias encontradas ({len(resultados)}):")
                for k, (m, l) in enumerate(resultados, 1):
                    print(f"{k}. {l.nombre} (Municipio: {m.nombre})")

                try:
                    idx_sel = int(input("\nSeleccione el número de la localidad deseada: ")) - 1
                    if 0 <= idx_sel < len(resultados):
                        mun_o, loc_o = resultados[idx_sel]
                        reg = ServicioApiClima.consultar_clima_actual(
                            mun_o.nombre, loc_o.nombre, loc_o.latitud, loc_o.longitud
                        )
                        if reg:
                            reg.mostrar_detalle()
                            gestor_stats.registrar_consulta(reg)
                    else:
                        print("\nOpción fuera de rango.")
                except ValueError:
                    print("\nIngrese un valor numérico.")

        elif opcion == "3":
            print("\nMÓDULO DE REPORTES Y ESTADÍSTICAS")
            gestor_stats.ranking_temperatura()
            gestor_stats.promedio_general_temperatura()
            gestor_stats.reporte_cobertura_geografica(municipios)

        elif opcion == "4":
            print("\nCONSULTA HISTÓRICA Y GRÁFICOS")
            query = input("Ingrese la localidad a analizar: ")
            resultados = buscar_localidades_por_nombre(municipios, query)

            if not resultados:
                print("\nNo se encontró la localidad especificada.")
            else:
                for k, (m, l) in enumerate(resultados, 1):
                    print(f"{k}. {l.nombre} ({m.nombre})")
                try:
                    sel = int(input("\nSeleccione el número: ")) - 1
                    if 0 <= sel < len(resultados):
                        _, loc_h = resultados[sel]
                        f_inicio = input("Fecha inicio (AAAA-MM-DD): ").strip()
                        f_fin = input("Fecha fin (AAAA-MM-DD): ").strip()

                        gestor_historico.consultar_y_graficar_historico(
                            loc_h.latitud, loc_h.longitud, loc_h.nombre, f_inicio, f_fin
                        )
                    else:
                        print("\nOpción no válida.")
                except ValueError:
                    print("\nEntrada no válida.")

        elif opcion == "5":
            print("\n¡Gracias por utilizar MeteoCaracas! Hasta luego.")
            break
        else:
            print("\nOpción no válida. Intente con un número entre 1 y 5.")

if __name__ == "__main__":
    ejecutar_menu_principal()