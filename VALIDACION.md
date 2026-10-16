# Verificación

**Fecha:** 16/10/2026

Ejecutado desde la raíz del repositorio:

```bash
python -m unittest discover -s tests -v
python src/main.py --entrada data/sesion_f1.csv --sin-graficos
```

Las **38 pruebas terminaron correctamente**, incluidas las tres de gráficos. La aplicación procesó la sesión de ejemplo: leyó 91 registros, aceptó 84, rechazó 7 y excluyó 4 vueltas. Los reportes se guardan en `outputs/`.
