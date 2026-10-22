# Entradas mal cargadas de ejemplo

Archivos con errores deliberados para practicar la guía [Si una entrada está mal cargada](../../README.md#si-una-entrada-está-mal-cargada). Todos terminan con código de salida `1`. Los mensajes reproducidos aquí se comprueban en `tests/test_pipeline.py`.

Desde la raíz del repositorio:

```bash
python src/main.py --entrada data/ejemplos_invalidos/<archivo> --salida /tmp/diagnostico --sin-graficos
```

| Archivo | Problema | Mensaje esperado |
|---|---|---|
| `sin_columna_tiempo.csv` | El encabezado no incluye la columna obligatoria `tiempo`. | `ERROR: Faltan columnas obligatorias: tiempo. Columnas encontradas: piloto, s1, s2, s3, vuelta.` |
| `json_roto.json` | Falta cerrar el último objeto y la lista. | `ERROR: El JSON '...' no es válido: Expecting ',' delimiter: ...` |
| `sesion.xlsx` | La extensión no es `.csv` ni `.json` (el contenido no se llega a leer). | `ERROR: Formato no soportado '.xlsx'. Use .csv o .json.` |
| `todas_invalidas.csv` | Cada fila tiene un error distinto, así que ninguna supera la validación. | `ERROR: Ningún registro superó la validación; revise el archivo de rechazos.` |

En el último caso el esquema es correcto, por eso igual se genera `rechazos.csv` con el motivo de cada fila:

| Registro | Motivo |
|---|---|
| 1 | `código de piloto inválido: 'VERS' (se esperan 3 letras)` |
| 2 | `número de vuelta inválido: '0'` |
| 3 | `número de vuelta inválido: '2.5'` |
| 4 | `vuelta incompleta (sin tiempo)` |
| 5 | `formato de tiempo no reconocido: '1:2x.000' (se esperaba M:SS.mmm o SS.mmm)` |
| 6 | `tiempo fuera de rango: 599.0 s (válido 30.0-300.0)` |
| 7 | `sectores incompletos (deben venir los tres)` |
