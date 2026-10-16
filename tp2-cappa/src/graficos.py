"""Gráficos del reporte (requiere matplotlib).

Este módulo es opcional: el resto de la aplicación usa sólo la biblioteca estándar.
Si matplotlib no está instalado, main.py avisa y continúa sin gráficos.
"""

import os
from typing import Dict, List, Sequence

import matplotlib

matplotlib.use("Agg")  # backend sin ventana: sólo guarda archivos PNG
import matplotlib.pyplot as plt  # noqa: E402

from modelos import Vuelta  # noqa: E402
from pipeline import segundos_a_texto  # noqa: E402

DPI = 130


def _guardar(fig, carpeta: str, nombre: str) -> str:
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)
    fig.tight_layout()
    fig.savefig(ruta, dpi=DPI)
    plt.close(fig)
    return ruta


def grafico_diferencia_mejor_vuelta(resultado: Sequence[Dict], carpeta: str) -> str:
    """Barras horizontales: diferencia de cada piloto con la mejor vuelta de la sesión."""
    datos = [f for f in resultado if f["mejor_s"] is not None]
    datos.sort(key=lambda f: f["dif_al_mejor_s"], reverse=True)  # el mejor queda arriba
    fig, ax = plt.subplots(figsize=(8, 4.5))
    barras = ax.barh(
        [f["piloto"] for f in datos],
        [f["dif_al_mejor_s"] for f in datos],
        color="#c0392b",
    )
    for barra, f in zip(barras, datos):
        ax.text(
            barra.get_width() + 0.01,
            barra.get_y() + barra.get_height() / 2,
            f"{segundos_a_texto(f['mejor_s'])} (vuelta {f['mejor_vuelta']})",
            va="center",
            fontsize=8,
        )
    ax.set_xlabel("Diferencia con la mejor vuelta de la sesión (s)")
    ax.set_title("Mejor vuelta por piloto")
    ax.set_xlim(0, max(f["dif_al_mejor_s"] for f in datos) * 1.45 + 0.05)
    return _guardar(fig, carpeta, "grafico_mejor_vuelta.png")


def grafico_evolucion(
    vueltas: Sequence[Vuelta],
    seleccion: Sequence[Vuelta],
    pilotos: Sequence[str],
    carpeta: str,
) -> str:
    """Tiempo por vuelta de cada piloto. Las vueltas excluidas se marcan con X (o ▲ si
    quedan fuera de la escala del gráfico)."""
    usadas = {(v.piloto, v.numero) for v in seleccion}
    tiempos_sel = [v.tiempo_s for v in seleccion] or [v.tiempo_s for v in vueltas]
    piso, techo = min(tiempos_sel) - 0.5, max(tiempos_sel) + 0.5

    fig, ax = plt.subplots(figsize=(9, 5))
    for i, piloto in enumerate(pilotos):
        color = f"C{i % 10}"
        propias = sorted(
            (v for v in vueltas if v.piloto == piloto), key=lambda v: v.numero
        )
        buenas = [v for v in propias if (v.piloto, v.numero) in usadas]
        ax.plot(
            [v.numero for v in buenas],
            [v.tiempo_s for v in buenas],
            marker="o",
            markersize=3.5,
            linewidth=1.2,
            color=color,
            label=piloto,
        )
        for v in propias:
            if (v.piloto, v.numero) in usadas:
                continue
            fuera = v.tiempo_s > techo
            ax.scatter(
                v.numero,
                min(v.tiempo_s, techo + 0.15),
                marker="^" if fuera else "x",
                s=45,
                color=color,
                zorder=3,
            )
    ax.set_ylim(piso, techo + 0.35)
    ax.set_xlabel("Número de vuelta")
    ax.set_ylabel("Tiempo (s)")
    ax.set_title(
        "Evolución del tiempo por vuelta\n(x = vuelta excluida, ▲ = excluida fuera de escala)"
    )
    ax.grid(alpha=0.3)
    ax.legend(ncol=3, fontsize=8)
    return _guardar(fig, carpeta, "grafico_evolucion_vueltas.png")


def grafico_dispersion(
    seleccion: Sequence[Vuelta], pilotos: Sequence[str], carpeta: str
) -> str:
    """Boxplot de los tiempos utilizados por piloto (ordenados por mediana)."""
    series = {p: [v.tiempo_s for v in seleccion if v.piloto == p] for p in pilotos}
    series = {p: t for p, t in series.items() if t}
    orden = sorted(series, key=lambda p: sorted(series[p])[len(series[p]) // 2])
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.boxplot([series[p] for p in orden], showmeans=True)
    ax.set_xticks(range(1, len(orden) + 1))
    ax.set_xticklabels(orden)
    ax.set_ylabel("Tiempo de vuelta (s)")
    ax.set_title(
        "Dispersión de los tiempos por piloto\n(línea = mediana, triángulo = media)"
    )
    ax.grid(axis="y", alpha=0.3)
    return _guardar(fig, carpeta, "grafico_dispersion.png")


def grafico_sectores(sectores: Sequence[Dict], carpeta: str) -> str:
    """Barras agrupadas: diferencia de cada piloto con el mejor tiempo de cada sector."""
    datos = [f for f in sectores if f["mejor_s1"] is not None]
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ancho = 0.25
    for i, clave in enumerate(("mejor_s1", "mejor_s2", "mejor_s3")):
        referencia = min(f[clave] for f in datos)
        posiciones = [j + (i - 1) * ancho for j in range(len(datos))]
        ax.bar(
            posiciones,
            [f[clave] - referencia for f in datos],
            ancho,
            label=f"Sector {i + 1}",
        )
    ax.set_xticks(range(len(datos)))
    ax.set_xticklabels([f["piloto"] for f in datos])
    ax.set_ylabel("Diferencia con el mejor del sector (s)")
    ax.set_title("Mejor tiempo por sector, respecto del más rápido")
    ax.legend()
    ax.grid(axis="y", alpha=0.3)
    return _guardar(fig, carpeta, "grafico_sectores.png")


def generar_graficos(
    vueltas: Sequence[Vuelta],
    seleccion: Sequence[Vuelta],
    pilotos: Sequence[str],
    resultado: Sequence[Dict],
    sectores: Sequence[Dict],
    carpeta: str,
) -> List[str]:
    """Genera los cuatro gráficos y devuelve las rutas creadas."""
    rutas = [
        grafico_diferencia_mejor_vuelta(resultado, carpeta),
        grafico_evolucion(vueltas, seleccion, pilotos, carpeta),
        grafico_dispersion(seleccion, pilotos, carpeta),
    ]
    if any(f["mejor_s1"] is not None for f in sectores):
        rutas.append(grafico_sectores(sectores, carpeta))
    return rutas
