"""Punto de entrada: validador de sesiones y comparador de vueltas.

Uso (desde la raíz del repositorio):
    python src/main.py --entrada data/sesion_f1.csv
    python src/main.py --entrada data/sesion_f1.json --pilotos VER NOR LEC --tolerancia 0.1
"""

import argparse
import os
import sys

from fuentes import fuente_para
from pipeline import (
    EsquemaInvalidoError,
    ResultadoInconsistenteError,
    comparar_pilotos,
    comparar_sectores,
    guardar_incidencias,
    guardar_rechazos,
    guardar_resultado,
    guardar_sectores,
    limpiar_datos,
    normalizar_campos,
    segundos_a_texto,
    seleccionar_vueltas,
    validar_esquema,
    verificar_resultado,
)


def construir_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Valida una sesión de vueltas y compara pilotos."
    )
    p.add_argument(
        "--entrada", required=True, help="ruta del archivo .csv o .json con las vueltas"
    )
    p.add_argument(
        "--pilotos",
        nargs="+",
        metavar="COD",
        help="códigos de piloto a comparar (por defecto, todos)",
    )
    p.add_argument(
        "--tolerancia",
        type=float,
        default=0.05,
        help="diferencia máxima (s) entre tiempo total y suma de sectores (default 0.05)",
    )
    p.add_argument(
        "--umbral-lenta",
        type=float,
        default=1.15,
        help="una vuelta es lenta si supera este múltiplo de la mediana del piloto (default 1.15)",
    )
    p.add_argument(
        "--salida", default="outputs", help="carpeta de salida (default: outputs)"
    )
    p.add_argument(
        "--sin-graficos",
        action="store_true",
        help="no generar gráficos (no requiere matplotlib)",
    )
    return p


def imprimir_tabla(resultado) -> None:
    print(
        f"\n{'Piloto':<7}{'Vueltas':>8}{'Mejor':>11}{'Media':>11}{'Desvío(s)':>11}{'Dif.mejor(s)':>14}  Nota"
    )
    for f in resultado:
        if f["mejor_s"] is None:
            print(
                f"{f['piloto']:<7}{f['n_vueltas']:>8}{'-':>11}{'-':>11}{'-':>11}{'-':>14}  {f['nota']}"
            )
            continue
        desvio = f"{f['desvio_s']:.3f}" if f["desvio_s"] is not None else "-"
        print(
            f"{f['piloto']:<7}{f['n_vueltas']:>8}{segundos_a_texto(f['mejor_s']):>11}"
            f"{segundos_a_texto(f['media_s']):>11}{desvio:>11}{f['dif_al_mejor_s']:>14.3f}  {f['nota']}"
        )


def main(argv=None) -> int:
    args = construir_parser().parse_args(argv)
    try:
        # leer
        filas = fuente_para(args.entrada).cargar(args.entrada)
        # inspeccionar y validar
        filas = normalizar_campos(filas)
        validar_esquema(filas)
        # limpiar y transformar
        vueltas, rechazos = limpiar_datos(filas)
        if not vueltas:
            raise ValueError(
                "Ningún registro superó la validación; revise el archivo de rechazos."
            )
        # analizar
        seleccion, incidencias = seleccionar_vueltas(
            vueltas, args.pilotos, args.tolerancia, args.umbral_lenta
        )
        pilotos = (
            [p.upper() for p in args.pilotos]
            if args.pilotos
            else sorted({v.piloto for v in vueltas})
        )
        resultado = comparar_pilotos(seleccion, pilotos)
        sectores = comparar_sectores(seleccion, pilotos)
        verificar_resultado(resultado, seleccion)
        # comunicar
        guardar_resultado(
            resultado, os.path.join(args.salida, "comparacion_pilotos.csv")
        )
        guardar_rechazos(rechazos, os.path.join(args.salida, "rechazos.csv"))
        guardar_incidencias(incidencias, os.path.join(args.salida, "incidencias.csv"))
        guardar_sectores(
            sectores, os.path.join(args.salida, "comparacion_sectores.csv")
        )
    except (
        FileNotFoundError,
        EsquemaInvalidoError,
        ValueError,
        ResultadoInconsistenteError,
    ) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Registros leídos:      {len(filas)}")
    print(f"Registros válidos:     {len(vueltas)}")
    print(
        f"Registros rechazados:  {len(rechazos)}  -> {os.path.join(args.salida, 'rechazos.csv')}"
    )
    print(
        f"Vueltas excluidas:     {len(incidencias)}  -> {os.path.join(args.salida, 'incidencias.csv')}"
    )
    print(f"Vueltas utilizadas:    {len(seleccion)}")
    imprimir_tabla(resultado)
    print(
        f"\nResultado guardado en {os.path.join(args.salida, 'comparacion_pilotos.csv')}"
    )
    print(
        f"Sectores guardados en {os.path.join(args.salida, 'comparacion_sectores.csv')}"
    )

    if not args.sin_graficos:
        try:
            from graficos import generar_graficos
        except ImportError:
            print(
                "AVISO: matplotlib no está instalado; se omiten los gráficos "
                "(pip install -r requirements.txt).",
                file=sys.stderr,
            )
        else:
            vueltas_sel = [v for v in vueltas if v.piloto in pilotos]
            rutas = generar_graficos(
                vueltas_sel, seleccion, pilotos, resultado, sectores, args.salida
            )
            print("Gráficos generados:")
            for ruta in rutas:
                print(f"  {ruta}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
