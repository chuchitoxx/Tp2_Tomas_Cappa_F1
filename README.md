# TP2: análisis de vueltas de Fórmula 1
TP2 de Programación Orientada a Datos (UCA, 2026): Aplicación en Python para validar registros de vueltas de telemetría de Fórmula 1 y comparar tiempos por piloto, vuelta o sector.

## Empezar (Windows)

1. Instala Python 3.9 o una versión más nueva, si todavía no lo tienes.
2. Abre esta carpeta y haz doble clic en `ejecutar.bat`.
3. Mira el resumen en la ventana. Los archivos con los resultados quedan en `outputs`.

No necesitas saber programar ni usar Git para ejecutar el programa.

Los gráficos son opcionales. Para instalarlos, abre una terminal en esta carpeta y ejecuta una sola vez:

```text
py -m pip install -r requirements.txt
```

Si no instalas los gráficos, el análisis igual funciona.

## Qué hace

- Revisa los datos y explica qué filas no se pueden usar.
- Compara los tiempos de los pilotos.
- Guarda tablas y, si está instalado matplotlib, gráficos en `outputs`.

## Resultado del ejemplo

La validación del archivo de ejemplo dejó un balance claro:

- 91 registros leídos
- 84 válidos
- 7 rechazados
- 4 vueltas excluidas por incidencias
- 80 vueltas utilizadas para comparar

Esto significa que la mayoría de los datos del archivo pudo usarse en la comparación final, y los descartes quedaron registrados en `outputs` para revisar qué falló.

### Ranking del ejemplo

1. VER — mejor vuelta: 1:24.675
2. NOR — mejor vuelta: 1:25.011
3. HAM — mejor vuelta: 1:25.248
4. RUS — mejor vuelta: 1:25.278
5. LEC — mejor vuelta: 1:25.440
6. ALO — mejor vuelta: 1:25.627

## Carpetas

- `data`: archivo de ejemplo.
- `src`: programa. Para empezar, no hace falta modificar estos archivos.
- `tests`: pruebas automáticas.
- `scripts`: herramienta para volver a generar los datos simulados.
- `docs`: ejemplos de gráficos.

## Si quieres ejecutarlo desde una terminal

Abre una terminal en esta carpeta y copia:

```text
py src\main.py
```

El archivo de ejemplo ya está seleccionado por defecto. Si quieres analizar otro archivo, puedes indicar su ruta con `--entrada`.

Para ejecutar las pruebas:

```text
py -m unittest discover -s tests -v
```

Consulta [ENTREGA.md](ENTREGA.md) para el checklist del trabajo y [VALIDACION.md](VALIDACION.md) para la comprobación realizada.
