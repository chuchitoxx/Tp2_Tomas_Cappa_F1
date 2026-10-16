"""Flujo de procesamiento: validar, limpiar, seleccionar, comparar y exportar."""

import csv
import os
import re
import statistics
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional, Sequence, Tuple

from modelos import Vuelta

# ---------------------------------------------------------------- constantes
COLUMNAS_OBLIGATORIAS = ("piloto", "vuelta", "tiempo")
COLUMNAS_SECTORES = ("s1", "s2", "s3")
TIEMPO_MIN_S = 30.0  # por debajo de esto el tiempo no es físicamente razonable
TIEMPO_MAX_S = 300.0  # por encima, no es una vuelta de carrera normal
VUELTA_MAX = 999

# Código de piloto: exactamente tres letras mayúsculas (ej. VER, NOR).
PATRON_PILOTO = re.compile(r"^[A-Z]{3}$")

# Tiempo de vuelta en dos escrituras: "M:SS.mmm" (1:25.123) o "SS.mmm" (85.123).
# La expresión regular sólo verifica la FORMA del texto; los rangos
# se comprueban aparte (ver limpiar_datos).
PATRON_TIEMPO = re.compile(
    r"^(?:(?P<min>\d{1,2}):(?P<seg>[0-5]\d)|(?P<seg_solo>\d{1,3}))\.(?P<ms>\d{1,3})$"
)


class EsquemaInvalidoError(ValueError):
    """El archivo no tiene las columnas necesarias."""


class ResultadoInconsistenteError(AssertionError):
    """El resultado calculado no cumple una propiedad esperada."""


# ------------------------------------------------------------ conversiones
def convertir_tiempo(texto) -> float:
    """Convierte "M:SS.mmm" o "SS.mmm" a segundos. Lanza ValueError si no es válido."""
    if texto is None or str(texto).strip() == "":
        raise ValueError("tiempo vacío")
    t = str(texto).strip()
    m = PATRON_TIEMPO.match(t)
    if not m:
        raise ValueError(
            f"formato de tiempo no reconocido: '{t}' (se esperaba M:SS.mmm o SS.mmm)"
        )
    fraccion = float("0." + m.group("ms"))
    if m.group("min") is not None:
        segundos = int(m.group("min")) * 60 + int(m.group("seg")) + fraccion
    else:
        segundos = int(m.group("seg_solo")) + fraccion
    return round(segundos, 3)


def segundos_a_texto(segundos: float) -> str:
    """Formatea segundos como M:SS.mmm."""
    minutos = int(segundos // 60)
    resto = segundos - minutos * 60
    return f"{minutos}:{resto:06.3f}"


def _convertir_sector(texto: str) -> float:
    try:
        valor = float(texto)
    except ValueError:
        raise ValueError(f"sector no numérico: '{texto}'")
    if not (0 < valor < TIEMPO_MAX_S):
        raise ValueError(f"sector fuera de rango: {valor}")
    return round(valor, 3)


# ------------------------------------------------------- normalizar / validar
def normalizar_campos(filas: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Encabezados en minúscula, valores sin espacios, piloto en mayúscula.

    Agrega '_registro' (posición 1..N en el archivo) para poder informar rechazos.
    """
    normalizadas = []
    for i, fila in enumerate(filas, start=1):
        nueva = {str(k).strip().lower(): str(v).strip() for k, v in fila.items()}
        if "piloto" in nueva:
            nueva["piloto"] = nueva["piloto"].upper()
        nueva["_registro"] = str(i)
        normalizadas.append(nueva)
    return normalizadas


def validar_esquema(filas: List[Dict[str, str]]) -> None:
    """Verifica que existan filas y las columnas obligatorias."""
    if not filas:
        raise EsquemaInvalidoError("El archivo no contiene registros.")
    presentes = set(filas[0].keys())
    faltantes = [c for c in COLUMNAS_OBLIGATORIAS if c not in presentes]
    if faltantes:
        raise EsquemaInvalidoError(
            f"Faltan columnas obligatorias: {', '.join(faltantes)}. "
            f"Columnas encontradas: {', '.join(sorted(c for c in presentes if not c.startswith('_')))}."
        )


# -------------------------------------------------------------------- limpieza
def limpiar_datos(
    filas: List[Dict[str, str]],
) -> Tuple[List[Vuelta], List[Dict[str, str]]]:
    """Convierte filas en objetos Vuelta y separa los registros rechazados.

    Reglas de rechazo (cada registro se rechaza una sola vez, por el primer motivo):
      1. código de piloto inválido (no cumple ^[A-Z]{3}$);
      2. número de vuelta no entero o fuera de [1, VUELTA_MAX];
      3. tiempo faltante (vuelta incompleta) o con formato inválido;
      4. tiempo fuera de [TIEMPO_MIN_S, TIEMPO_MAX_S];
      5. sectores incompletos o inválidos (se aceptan 0 o los 3 sectores);
      6. duplicado de (piloto, vuelta): se conserva el primer registro.
    Nunca se descarta nada en silencio: cada rechazo queda con su motivo.
    """
    vueltas: List[Vuelta] = []
    rechazos: List[Dict[str, str]] = []
    vistos: Dict[Tuple[str, int], str] = {}

    def rechazar(fila, motivo):
        rechazos.append(
            {
                "registro": fila.get("_registro", ""),
                "piloto": fila.get("piloto", ""),
                "vuelta": fila.get("vuelta", ""),
                "motivo": motivo,
            }
        )

    for fila in filas:
        piloto = fila.get("piloto", "")
        if not PATRON_PILOTO.match(piloto):
            rechazar(
                fila, f"código de piloto inválido: '{piloto}' (se esperan 3 letras)"
            )
            continue

        try:
            numero_decimal = Decimal(fila.get("vuelta", ""))
            if (
                not numero_decimal.is_finite()
                or numero_decimal < 1
                or numero_decimal > VUELTA_MAX
                or numero_decimal != numero_decimal.to_integral_value()
            ):
                raise ValueError
            numero = int(numero_decimal)
        except (InvalidOperation, ValueError):
            rechazar(fila, f"número de vuelta inválido: '{fila.get('vuelta', '')}'")
            continue

        try:
            tiempo = convertir_tiempo(fila.get("tiempo", ""))
        except ValueError as e:
            motivo = (
                "vuelta incompleta (sin tiempo)" if str(e) == "tiempo vacío" else str(e)
            )
            rechazar(fila, motivo)
            continue
        if not (TIEMPO_MIN_S <= tiempo <= TIEMPO_MAX_S):
            rechazar(
                fila,
                f"tiempo fuera de rango: {tiempo} s (válido {TIEMPO_MIN_S}-{TIEMPO_MAX_S})",
            )
            continue

        crudos = [fila.get(c, "") for c in COLUMNAS_SECTORES]
        sectores: Optional[List[float]] = None
        if any(crudos):
            try:
                if not all(crudos):
                    raise ValueError("sectores incompletos (deben venir los tres)")
                sectores = [_convertir_sector(s) for s in crudos]
            except ValueError as e:
                rechazar(fila, str(e))
                continue

        clave = (piloto, numero)
        if clave in vistos:
            rechazar(
                fila,
                f"duplicado de {piloto} vuelta {numero} (ya figura en el registro {vistos[clave]})",
            )
            continue
        vistos[clave] = fila.get("_registro", "")

        vueltas.append(Vuelta(piloto, numero, tiempo, sectores))

    return vueltas, rechazos


# ------------------------------------------------------------------- selección
def seleccionar_vueltas(
    vueltas: Sequence[Vuelta],
    pilotos: Optional[Sequence[str]] = None,
    tolerancia: float = 0.05,
    umbral_lenta: float = 1.15,
) -> Tuple[List[Vuelta], List[Dict[str, str]]]:
    """Aplica las exclusiones documentadas y devuelve (seleccion, incidencias).

    Exclusiones (cada una queda registrada como incidencia):
      * sectores inconsistentes: |tiempo - (s1+s2+s3)| > tolerancia;
      * vuelta lenta: tiempo > umbral_lenta * mediana del piloto (posible vuelta de
        salida/entrada a boxes). Sólo se evalúa si el piloto tiene al menos 3 vueltas.
    """
    if tolerancia < 0:
        raise ValueError("La tolerancia no puede ser negativa.")
    if umbral_lenta <= 1:
        raise ValueError("El umbral de vuelta lenta debe ser mayor que 1.")

    disponibles = sorted({v.piloto for v in vueltas})
    if pilotos:
        elegidos = [p.upper() for p in pilotos]
        invalidos = [p for p in elegidos if not PATRON_PILOTO.match(p)]
        if invalidos:
            raise ValueError(f"Código(s) de piloto inválido(s): {', '.join(invalidos)}")
        desconocidos = [p for p in elegidos if p not in disponibles]
        if desconocidos:
            raise ValueError(
                f"Sin datos para: {', '.join(desconocidos)}. Pilotos disponibles: {', '.join(disponibles)}"
            )
    else:
        elegidos = disponibles

    seleccion: List[Vuelta] = []
    incidencias: List[Dict[str, str]] = []

    for piloto in elegidos:
        propias = sorted(
            (v for v in vueltas if v.piloto == piloto), key=lambda v: v.numero
        )
        mediana = (
            statistics.median(v.tiempo_s for v in propias)
            if len(propias) >= 3
            else None
        )
        for v in propias:
            if not v.es_consistente(tolerancia):
                incidencias.append(
                    {
                        "piloto": piloto,
                        "vuelta": str(v.numero),
                        "tipo": "sectores inconsistentes",
                        "detalle": (
                            f"tiempo {v.tiempo_s:.3f} s vs suma de sectores {v.suma_sectores():.3f} s "
                            f"(diferencia {v.diferencia_sectores():.3f} s > tolerancia {tolerancia} s)"
                        ),
                    }
                )
            elif mediana is not None and v.tiempo_s > umbral_lenta * mediana:
                incidencias.append(
                    {
                        "piloto": piloto,
                        "vuelta": str(v.numero),
                        "tipo": "vuelta lenta",
                        "detalle": (
                            f"tiempo {v.tiempo_s:.3f} s supera {umbral_lenta}x la mediana "
                            f"del piloto ({mediana:.3f} s); posible vuelta de boxes"
                        ),
                    }
                )
            else:
                seleccion.append(v)
    return seleccion, incidencias


# ------------------------------------------------------------------ comparación
def comparar_pilotos(seleccion: Sequence[Vuelta], pilotos: Sequence[str]) -> List[Dict]:
    """Calcula mejor vuelta, media y dispersión por piloto, ordenado por mejor vuelta.

    Casos explícitos:
      * 0 vueltas utilizables  -> estadísticos None y nota "sin vueltas utilizables";
      * 1 vuelta utilizable    -> desvío None y nota "dispersión no definida".
    """
    resultado = []
    for piloto in pilotos:
        propias = sorted(
            (v for v in seleccion if v.piloto == piloto), key=lambda v: v.numero
        )
        fila = {
            "piloto": piloto,
            "n_vueltas": len(propias),
            "vueltas_usadas": " ".join(str(v.numero) for v in propias),
            "mejor_vuelta": None,
            "mejor_s": None,
            "media_s": None,
            "desvio_s": None,
            "dif_al_mejor_s": None,
            "nota": "",
        }
        if not propias:
            fila["nota"] = "sin vueltas utilizables"
        else:
            mejor = min(propias, key=lambda v: v.tiempo_s)
            tiempos = [v.tiempo_s for v in propias]
            fila["mejor_vuelta"] = mejor.numero
            fila["mejor_s"] = round(mejor.tiempo_s, 3)
            fila["media_s"] = round(statistics.mean(tiempos), 3)
            if len(propias) >= 2:
                fila["desvio_s"] = round(statistics.stdev(tiempos), 3)
            else:
                fila["nota"] = "una sola vuelta válida: dispersión no definida"
        resultado.append(fila)

    con_datos = [f for f in resultado if f["mejor_s"] is not None]
    if con_datos:
        referencia = min(f["mejor_s"] for f in con_datos)
        for f in con_datos:
            f["dif_al_mejor_s"] = round(f["mejor_s"] - referencia, 3)

    resultado.sort(
        key=lambda f: (
            f["mejor_s"] is None,
            f["mejor_s"] if f["mejor_s"] is not None else 0,
            f["piloto"],
        )
    )
    return resultado


def comparar_sectores(
    seleccion: Sequence[Vuelta], pilotos: Sequence[str]
) -> List[Dict]:
    """Mejor tiempo de cada sector por piloto y 'vuelta ideal' (suma de sus mejores sectores).

    Sólo usa vueltas de la selección que tengan los tres sectores. Si un piloto no
    tiene ninguna, sus campos quedan en None.
    """
    filas = []
    for piloto in pilotos:
        con = [v for v in seleccion if v.piloto == piloto and v.tiene_sectores()]
        fila = {
            "piloto": piloto,
            "n_vueltas_con_sectores": len(con),
            "mejor_s1": None,
            "mejor_s2": None,
            "mejor_s3": None,
            "vuelta_ideal_s": None,
        }
        if con:
            mejores = [round(min(v.sectores[i] for v in con), 3) for i in range(3)]
            fila.update(
                mejor_s1=mejores[0],
                mejor_s2=mejores[1],
                mejor_s3=mejores[2],
                vuelta_ideal_s=round(sum(mejores), 3),
            )
        filas.append(fila)
    return filas


def verificar_resultado(resultado: Sequence[Dict], seleccion: Sequence[Vuelta]) -> None:
    """Comprueba propiedades del resultado; lanza ResultadoInconsistenteError si fallan."""
    pilotos = {f["piloto"] for f in resultado}
    esperadas = sum(1 for v in seleccion if v.piloto in pilotos)
    if sum(f["n_vueltas"] for f in resultado) != esperadas:
        raise ResultadoInconsistenteError(
            "La cantidad de vueltas del resultado no coincide con la selección."
        )
    for f in resultado:
        if len(f["vueltas_usadas"].split()) != f["n_vueltas"]:
            raise ResultadoInconsistenteError(
                f"{f['piloto']}: lista de vueltas usadas incoherente."
            )
        if f["n_vueltas"] == 0:
            continue
        if not (TIEMPO_MIN_S <= f["mejor_s"] <= f["media_s"]):
            raise ResultadoInconsistenteError(
                f"{f['piloto']}: se esperaba mejor <= media."
            )
        if f["desvio_s"] is not None and f["desvio_s"] < 0:
            raise ResultadoInconsistenteError(f"{f['piloto']}: desvío negativo.")


# ------------------------------------------------------------------ exportación
def _guardar_csv(ruta: str, filas: Sequence[Dict], columnas: Sequence[str]) -> None:
    carpeta = os.path.dirname(ruta)
    if carpeta:
        os.makedirs(carpeta, exist_ok=True)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.DictWriter(f, fieldnames=columnas, extrasaction="ignore")
        escritor.writeheader()
        for fila in filas:
            escritor.writerow(
                {c: ("" if fila.get(c) is None else fila.get(c)) for c in columnas}
            )


def guardar_resultado(resultado: Sequence[Dict], ruta: str) -> None:
    _guardar_csv(
        ruta,
        resultado,
        [
            "piloto",
            "n_vueltas",
            "vueltas_usadas",
            "mejor_vuelta",
            "mejor_s",
            "media_s",
            "desvio_s",
            "dif_al_mejor_s",
            "nota",
        ],
    )


def guardar_rechazos(rechazos: Sequence[Dict], ruta: str) -> None:
    _guardar_csv(ruta, rechazos, ["registro", "piloto", "vuelta", "motivo"])


def guardar_incidencias(incidencias: Sequence[Dict], ruta: str) -> None:
    _guardar_csv(ruta, incidencias, ["piloto", "vuelta", "tipo", "detalle"])


def guardar_sectores(sectores: Sequence[Dict], ruta: str) -> None:
    _guardar_csv(
        ruta,
        sectores,
        [
            "piloto",
            "n_vueltas_con_sectores",
            "mejor_s1",
            "mejor_s2",
            "mejor_s3",
            "vuelta_ideal_s",
        ],
    )
