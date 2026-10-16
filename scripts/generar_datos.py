"""Genera la sesión simulada data/sesion_f1.csv y data/sesion_f1.json.

Los datos son SIMULADOS (semilla fija) y se parecen a una sesión de Fórmula 1:
6 pilotos, 15 vueltas cada uno, tres sectores por vuelta. Se inyectan errores
conocidos para poder demostrar la validación (ver data/DATOS.md).

Uso (desde la raíz del repositorio):
    python scripts/generar_datos.py
"""

import csv
import json
import os
import random

SEMILLA = 2026
PILOTOS = {  # código: ritmo base (s) -> diferencia de ritmo entre pilotos
    "VER": 84.90,
    "NOR": 85.10,
    "LEC": 85.25,
    "HAM": 85.40,
    "RUS": 85.55,
    "ALO": 85.90,
}
VUELTAS = 15
CAMPOS = ["piloto", "vuelta", "tiempo", "s1", "s2", "s3"]


def a_texto(segundos: float, estilo: str) -> str:
    """Escribe el tiempo como 'M:SS.mmm' o como 'SS.mmm' (dos escrituras distintas)."""
    if estilo == "corto":
        return f"{segundos:.3f}"
    minutos = int(segundos // 60)
    return f"{minutos}:{segundos - minutos * 60:06.3f}"


def generar_filas():
    rng = random.Random(SEMILLA)
    filas = []
    for piloto, base in PILOTOS.items():
        for n in range(1, VUELTAS + 1):
            tiempo = round(
                base + rng.uniform(-0.4, 0.9) + 0.02 * n, 3
            )  # leve degradación de gomas
            s1 = round(tiempo * 0.33, 3)
            s2 = round(tiempo * 0.40, 3)
            s3 = round(tiempo - s1 - s2, 3)
            estilo = "corto" if rng.random() < 0.25 else "largo"
            filas.append(
                {
                    "piloto": piloto,
                    "vuelta": str(n),
                    "tiempo": a_texto(tiempo, estilo),
                    "s1": f"{s1:.3f}",
                    "s2": f"{s2:.3f}",
                    "s3": f"{s3:.3f}",
                }
            )

    def buscar(piloto, n):
        return next(f for f in filas if f["piloto"] == piloto and f["vuelta"] == str(n))

    # --- vueltas lentas válidas (salida / entrada a boxes) ---
    for piloto, n, t in (
        ("ALO", 1, 112.480),
        ("ALO", 8, 118.205),
        ("LEC", 15, 109.870),
    ):
        f = buscar(piloto, n)
        f["tiempo"] = a_texto(t, "largo")
        f["s1"], f["s2"] = f"{t * 0.33:.3f}", f"{t * 0.40:.3f}"
        f["s3"] = f"{t - round(t * 0.33, 3) - round(t * 0.40, 3):.3f}"

    # --- errores inyectados (cada uno se rechaza o marca por una regla distinta) ---
    buscar("NOR", 5)["tiempo"] = "1:2x.456"  # formato inválido
    buscar("LEC", 9)["tiempo"] = ""  # vuelta incompleta
    buscar("HAM", 3)["piloto"] = "H4M"  # código de piloto inválido
    buscar("NOR", 12)["tiempo"] = "0:12.345"  # fuera de rango (< 30 s)
    buscar("LEC", 4)["vuelta"] = "0"  # número de vuelta inválido
    buscar("ALO", 12)["s3"] = ""  # sectores incompletos
    r = buscar("RUS", 11)  # sectores inconsistentes (+0.8 s)
    r["s2"] = f"{float(r['s2']) + 0.8:.3f}"
    filas.insert(
        filas.index(buscar("VER", 7)) + 1, dict(buscar("VER", 7))
    )  # duplicado exacto
    return filas


def main():
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
    filas = generar_filas()
    with open(
        os.path.join(carpeta, "sesion_f1.csv"), "w", newline="", encoding="utf-8"
    ) as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        w.writerows(filas)
    with open(os.path.join(carpeta, "sesion_f1.json"), "w", encoding="utf-8") as f:
        json.dump(filas, f, ensure_ascii=False, indent=2)
    print(
        f"Generados {len(filas)} registros en data/sesion_f1.csv y data/sesion_f1.json"
    )


if __name__ == "__main__":
    main()
