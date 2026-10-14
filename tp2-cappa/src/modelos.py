"""Modelo del dominio: una vuelta de una sesión de automovilismo."""

from typing import List, Optional


class Vuelta:
    """Representa una vuelta cronometrada de un piloto.

    Atributos:
        piloto: código de tres letras (ej. "VER").
        numero: número de vuelta (entero positivo).
        tiempo_s: tiempo total en segundos.
        sectores: lista [s1, s2, s3] en segundos, o None si no se registraron.
    """

    def __init__(self, piloto: str, numero: int, tiempo_s: float,
                 sectores: Optional[List[float]] = None):
        self.piloto = piloto
        self.numero = numero
        self.tiempo_s = tiempo_s
        self.sectores = sectores

    def tiene_sectores(self) -> bool:
        return self.sectores is not None and len(self.sectores) == 3

    def suma_sectores(self) -> Optional[float]:
        """Suma de los tres sectores, o None si la vuelta no tiene sectores."""
        if not self.tiene_sectores():
            return None
        return round(sum(self.sectores), 3)

    def diferencia_sectores(self) -> Optional[float]:
        """Diferencia absoluta entre el tiempo total y la suma de sectores."""
        suma = self.suma_sectores()
        if suma is None:
            return None
        return round(abs(self.tiempo_s - suma), 3)

    def es_consistente(self, tolerancia: float) -> bool:
        """True si no hay sectores o si la diferencia está dentro de la tolerancia."""
        dif = self.diferencia_sectores()
        return dif is None or dif <= tolerancia

    def __repr__(self) -> str:
        return f"Vuelta({self.piloto}, n={self.numero}, {self.tiempo_s:.3f}s)"
