# TP2: comparador de vueltas de Fórmula 1

Aplicación de consola para validar una sesión de vueltas y comparar el rendimiento de sus pilotos. El proyecto está dentro de `tp2-cappa/`.

## Ejecutar

```bash
cd tp2-cappa
python src/main.py --entrada data/sesion_f1.csv --sin-graficos
```

Para ejecutar las pruebas:

```bash
python -m unittest discover -s tp2-cappa/tests -v
```

El [README del proyecto](tp2-cappa/README.md) explica las opciones, los datos y los resultados. La [validación](tp2-cappa/VALIDACION.md) y el [cotejo con la consigna](tp2-cappa/ENTREGA.md) tienen más detalles.
