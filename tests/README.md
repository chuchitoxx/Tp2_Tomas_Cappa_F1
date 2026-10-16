# Pruebas

Desde la raíz del repositorio, ejecutar:

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

La cantidad y el resultado de las pruebas ejecutadas se registran en `VALIDACION.md`. Si falta `matplotlib`, las pruebas de gráficos se omiten. Para instalarlo junto con la dependencia, ejecutar `pip install -r requirements.txt`.
