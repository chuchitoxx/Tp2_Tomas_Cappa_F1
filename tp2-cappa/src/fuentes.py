"""Fuentes de datos: abstracción común y dos implementaciones (CSV y JSON).

Contrato: FuenteDatos.cargar(ruta) devuelve una lista de diccionarios con
claves de texto y valores de texto (los valores ausentes quedan como "").
Así el resto de la aplicación no depende del formato del archivo de origen.
"""

import csv
import json
import os
from abc import ABC, abstractmethod
from typing import Dict, List

Fila = Dict[str, str]


class FuenteDatos(ABC):
    """Interfaz común para cualquier origen de datos tabulares."""

    @abstractmethod
    def cargar(self, ruta: str) -> List[Fila]:
        """Lee el archivo y devuelve una lista de diccionarios (texto)."""

    @staticmethod
    def _verificar_archivo(ruta: str) -> None:
        if not os.path.isfile(ruta):
            raise FileNotFoundError(f"No se encontró el archivo de entrada: '{ruta}'")


class FuenteCSV(FuenteDatos):
    """Lee un CSV con encabezado (UTF-8, con o sin BOM)."""

    def cargar(self, ruta: str) -> List[Fila]:
        self._verificar_archivo(ruta)
        with open(ruta, newline="", encoding="utf-8-sig") as f:
            lector = csv.DictReader(f)
            if lector.fieldnames is None:
                raise ValueError(f"El CSV '{ruta}' está vacío o no tiene encabezado.")
            lector.fieldnames = [nombre.strip() for nombre in lector.fieldnames]
            return [{k: (v if v is not None else "") for k, v in fila.items()}
                    for fila in lector]


class FuenteJSON(FuenteDatos):
    """Lee un JSON con una lista de objetos (o {"vueltas": [...]}).

    Los valores se convierten a texto (None -> "") para que la salida sea
    idéntica a la de FuenteCSV con los mismos datos.
    """

    def cargar(self, ruta: str) -> List[Fila]:
        self._verificar_archivo(ruta)
        with open(ruta, encoding="utf-8-sig") as f:
            try:
                contenido = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"El JSON '{ruta}' no es válido: {e}") from e
        if isinstance(contenido, dict) and isinstance(contenido.get("vueltas"), list):
            contenido = contenido["vueltas"]
        if not isinstance(contenido, list) or not all(isinstance(o, dict) for o in contenido):
            raise ValueError(
                f"El JSON '{ruta}' debe ser una lista de objetos "
                "(o un objeto con la clave 'vueltas')."
            )
        return [{str(k): ("" if v is None else str(v)) for k, v in obj.items()}
                for obj in contenido]


def fuente_para(ruta: str) -> FuenteDatos:
    """Elige la implementación según la extensión del archivo."""
    extension = os.path.splitext(ruta)[1].lower()
    if extension == ".csv":
        return FuenteCSV()
    if extension == ".json":
        return FuenteJSON()
    raise ValueError(f"Formato no soportado '{extension}'. Use .csv o .json.")
