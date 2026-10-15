# Pruebas

Desde la carpeta `tp2-cappa/`, ejecutar:

```bash
python -m unittest discover -s tests -v
```

## Qué cubren

- Lectura de CSV y JSON, incluida la equivalencia entre ambos formatos.
- Conversión de tiempos, validación de filas y registro de rechazos.
- Selección de vueltas, comparación de pilotos y cálculo de sectores.
- Casos límite, como una sola vuelta válida o un piloto sin vueltas utilizables.
- Propiedades del resultado: se conservan los registros y los estadísticos son coherentes.
- Gráficos, cuando `matplotlib` está instalado.

La última ejecución encontró **35 pruebas correctas**, incluidas las tres de gráficos. Si falta `matplotlib`, estas pruebas se omiten. Para instalarlo junto con la dependencia, ejecutar `pip install -r requirements.txt`.
