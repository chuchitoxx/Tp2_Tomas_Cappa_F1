# Validación del proyecto

## Comandos ejecutados

```bash
cd tp2-cappa
python -m unittest discover -s tests -v
python src/main.py --entrada data/sesion_f1.csv --sin-graficos
```

## Resultado verificado

- Las 35 pruebas finalizan correctamente; 3 pruebas de gráficos se omiten si `matplotlib` no está instalado.
- La aplicación principal ejecuta la sesión de ejemplo sin errores.
- La sesión produce 91 registros leídos, 84 válidos, 7 rechazados y 4 vueltas excluidas.
- Los archivos de salida se generan en `outputs/`.
