# TP2 - Validador de sesiones y comparador de vueltas

Este repositorio contiene el proyecto del Trabajo Práctico 2 de Programación Orientada a Datos.

## Estructura

- `tp2-cappa/` — proyecto principal con código fuente, datos y pruebas.

## Proyecto principal

La aplicación se ejecuta dentro de la carpeta `tp2-cappa`:

```bash
cd tp2-cappa
python src/main.py --entrada data/sesion_f1.csv
```

## Objetivo

Analizar una sesión de Fórmula 1 simulada, validar registros, excluir vueltas problemáticas y comparar pilotos mediante métricas de rendimiento.

## Estado

Este repositorio queda preparado para versionado y entrega del trabajo final.

## Verificación final

Validado el 2026-10-15 con `python -m unittest discover -s tests -v` y ejecución real de la aplicación: 35 pruebas correctas; 3 pruebas de gráficos se omitieron porque `matplotlib` no está instalado.

## Verificación rápida

```bash
cd tp2-cappa
python -m unittest discover -s tests -v
python src/main.py --entrada data/sesion_f1.csv --sin-graficos
```

La evidencia de ejecución queda documentada en `tp2-cappa/VALIDACION.md`.

## Checklist de entrega

La preparación del trabajo final queda resumida en `tp2-cappa/ENTREGA.md`.
