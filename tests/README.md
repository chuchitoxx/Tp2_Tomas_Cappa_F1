# Pruebas

La suite automatizada verifica funciones y comportamientos de la aplicación. Algunos tests cargan `data/sesion_f1.csv` y `data/sesion_f1.json` como conjunto de datos de prueba para comprobar lectura, conservación de registros y equivalencia entre formatos; otros usan filas preparadas dentro del propio test.

Desde la raíz del repositorio, ejecutar:

```bash
python -m unittest discover -s tests -v
```

## Qué cubren

- Lectura de CSV y JSON, incluida la equivalencia entre ambos formatos.
- Conversión de tiempos, validación de filas y registro de rechazos.
- Selección de vueltas, comparación de pilotos y cálculo de sectores.
- Casos límite, como una sola vuelta válida o un piloto sin vueltas utilizables.
- Entradas mal cargadas de `data/ejemplos_invalidos/`: terminan con código de salida 1 y el mensaje documentado.
- Propiedades del resultado: se conservan los registros y los estadísticos son coherentes.
- Gráficos, cuando `matplotlib` está instalado.

La cantidad y el resultado de las pruebas ejecutadas se registran en `VALIDACION.md`. Si falta `matplotlib`, las pruebas de gráficos se omiten. Para instalarlo junto con la dependencia, ejecutar `pip install -r requirements.txt`.

Un resultado `OK` confirma que los casos automatizados cubiertos pasaron en ese entorno. Para revisar cómo responde el programa ante una entrada nueva y diagnosticar filas rechazadas, seguí la guía [Si una entrada está mal cargada](../README.md#si-una-entrada-está-mal-cargada).
