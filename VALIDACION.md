# Verificación

**Fecha:** 20/10/2026
**Entorno:** Linux, Python 3.14.2

Ejecutado desde la raíz del repositorio. Se comprobó también la equivalencia de los reportes CSV y JSON:

```bash
python3 -m unittest discover -s tests -v
python3 src/main.py --entrada data/sesion_f1.csv --salida /tmp/tp2-final-csv --sin-graficos
python3 src/main.py --entrada data/sesion_f1.json --salida /tmp/tp2-final-json --sin-graficos
diff -u /tmp/tp2-final-csv/comparacion_pilotos.csv /tmp/tp2-final-json/comparacion_pilotos.csv
```

Las **39 pruebas terminaron correctamente**, incluidas las tres de gráficos. Los dos formatos produjeron reportes de comparación equivalentes. La aplicación procesó la sesión de ejemplo: leyó 91 registros, aceptó 84, rechazó 7 y excluyó 4 vueltas, con 80 vueltas utilizadas. Los reportes se guardan en `outputs/`.
