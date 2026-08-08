"""
En este archivo se define la estructura principal del proyecto mediante
clases de POO. Aquí se crean los municipios, las localidades y los reportes de clima, asegurándonos de guardar todo en objetos.
"""

class Localidad:
    # Representa una localidad o zona dentro de un municipio.

    # Atributos de la Clase Localidad.
    def __init__(self, nombre: str, latitud: float | None = None, longitud: float | None = None):
        # Guardamos el nombre y las coordenadas que vienen del JSON
        self.nombre: str = nombre
        self.latitud: float | None = latitud
        self.longitud: float | None = longitud


    def tiene_coordenadas(self) -> bool:
        # Verifica si la localidad tiene latitud y longitud válidas.
        # True si latitud y longitud no son None, False en caso contrario.
        return self.latitud is not None and self.longitud is not None

class Municipio:
    # Representa un municipio del Área Metropolitana de Caracas.
    
    # Atributos de la Clase Municipio. 
    def __init__(self, nombre: str, localidades: list[Localidad] | None = None):
        self.nombre: str = nombre
        self.localidades: list[Localidad] = localidades if localidades is not None else []

    def agregar_localidad(self, localidad: Localidad) -> None:
        # Agrega un objeto de la clase Localidad a la lista del municipio.
        self.localidades.append(localidad)

    def obtener_total_localidades(self) -> int:
        # Retorna la cantidad total de localidades registradas.
        return len(self.localidades)

    def obtener_localidades_con_coordenadas(self) -> list[Localidad]:
        # Filtra y retorna solo las localidades que tienen latitud y longitud.
        return [loc for loc in self.localidades if loc.tiene_coordenadas()]


    def obtener_localidades_sin_coordenadas(self) -> list[Localidad]:
        # Filtra y retorna solo las localidades que no poseen coordenadas.
        return [loc for loc in self.localidades if not loc.tiene_coordenadas()]


    def calcular_porcentaje_coordenadas(self) -> float:
        # Calcula el porcentaje de cobertura de coordenadas en el municipio.
        total = self.obtener_total_localidades()
        if total == 0:
            return 0.0
        con_coords = len(self.obtener_localidades_con_coordenadas())
        return (con_coords / total) * 100.0