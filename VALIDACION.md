# Verificación

**Fecha:** 21/10/2026
**Entorno:** Linux, Python 3.14.2

Este documento registra la suite automatizada y una prueba de integración del flujo completo con el conjunto de datos de prueba. Las filas inválidas del CSV/JSON son casos intencionales y sus rechazos forman parte del resultado esperado.

Ejecutado desde la raíz del repositorio. Se comprobó también la equivalencia de los reportes CSV y JSON:

```bash
python -m unittest discover -s tests
python3 src/main.py --entrada data/sesion_f1.csv --salida /tmp/tp2-entrega-final-csv --sin-graficos
python3 src/main.py --entrada data/sesion_f1.json --salida /tmp/tp2-entrega-final-json --sin-graficos
diff -u /tmp/tp2-entrega-final-csv/comparacion_pilotos.csv /tmp/tp2-entrega-final-json/comparacion_pilotos.csv
```

**Suite automatizada:** las 39 pruebas terminaron correctamente, incluidas las tres de gráficos.

**Prueba de integración CSV/JSON:** ambos formatos produjeron reportes de comparación equivalentes. La aplicación leyó 91 registros, aceptó 84, rechazó 7 y excluyó 4 vueltas, con 80 vueltas utilizadas. Los reportes se guardan en `outputs/`.
