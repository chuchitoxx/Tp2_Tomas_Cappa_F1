# Validación del proyecto

## Comandos ejecutados

```bash
cd /workspaces/aaa/tp2-cappa
pytest -q
python src/main.py --entrada data/sesion_f1.csv --sin-graficos
```

## Resultado verificado

- La suite de pruebas finaliza correctamente.
- La aplicación principal ejecuta la sesión de ejemplo sin errores.
- Los archivos de salida se generan en `outputs/`.
