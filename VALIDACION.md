# Comprobación del proyecto

Se ejecutaron las pruebas y el programa con los datos de ejemplo.

Para repetir la comprobación, abre una terminal en esta carpeta y ejecuta:

```text
py -m unittest discover -s tests -v
py src\main.py --entrada data\sesion_f1.csv --sin-graficos
```

## Resumen del resultado

La validación del archivo de ejemplo dejó un balance muy claro:

- 91 registros leídos
- 84 registros válidos
- 7 registros rechazados
- 4 vueltas excluidas por incidencias
- 80 vueltas utilizadas para comparar

En otras palabras, casi el 92% de los registros pudieron usarse para la comparación final, mientras que el resto quedó descartado por inconsistencias o datos no utilizables.

### Ranking del ejemplo

1. VER — mejor vuelta: 1:24.675, media: 1:25.318
2. NOR — mejor vuelta: 1:25.011, media: 1:25.409
3. HAM — mejor vuelta: 1:25.248, media: 1:25.738
4. RUS — mejor vuelta: 1:25.278, media: 1:26.040
5. LEC — mejor vuelta: 1:25.440, media: 1:25.750
6. ALO — mejor vuelta: 1:25.627, media: 1:26.176

Las tablas de resultados y los archivos de salida se guardan en `outputs`.
