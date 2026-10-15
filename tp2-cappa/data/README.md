# Datos

## Archivos

| Archivo | Descripción |
|---|---|
| `sesion_f1.csv` | Sesión simulada de 91 registros (formato CSV). |
| `sesion_f1.json` | Los mismos 91 registros en formato JSON (lista de objetos). Sirve para comprobar que ambas lecturas son equivalentes. |

## Procedencia

- **Tipo de datos:** datos **generados mediante una simulación**. No son tiempos reales de ninguna carrera.
- **Procedimiento de obtención:** `python scripts/generar_datos.py` (semilla fija `2026`, por lo que el resultado es siempre el mismo).
- **Responsable:** Tomás Cappa.
- **Licencia / condiciones de uso:** obra propia, de libre uso para fines académicos. No contiene datos personales: los códigos de piloto (VER, NOR, LEC, HAM, RUS, ALO) se usan sólo como etiquetas de formato.
- **Fecha de generación:** 13/10/2026.

## Unidad de análisis

Cada fila es **una vuelta cronometrada de un piloto** en una sesión.

## Variables

| Columna | Tipo | Descripción | Obligatoria |
|---|---|---|---|
| `piloto` | texto | Código de 3 letras mayúsculas (ej. `VER`). | Sí |
| `vuelta` | entero ≥ 1 | Número de vuelta dentro de la sesión. | Sí |
| `tiempo` | texto | Tiempo total de la vuelta, `M:SS.mmm` (`1:25.123`) o `SS.mmm` (`85.123`). | Sí |
| `s1`, `s2`, `s3` | decimal (s) | Tiempo de cada sector en segundos. Se aceptan los tres o ninguno. | No |

## Contenido

- 6 pilotos × 15 vueltas = 90 vueltas, más 1 registro duplicado = **91 observaciones**.
- Dos escrituras distintas del tiempo (aprox. 25 % en formato corto `SS.mmm`).

## Errores inyectados a propósito

Sirven para demostrar la validación (el reporte debe rechazar 7 registros y excluir 4 vueltas):

| Caso | Dónde | Resultado esperado |
|---|---|---|
| Registro duplicado | VER, vuelta 7 | Rechazado (duplicado) |
| Formato de tiempo inválido (`1:2x.456`) | NOR, vuelta 5 | Rechazado |
| Tiempo fuera de rango (`0:12.345`) | NOR, vuelta 12 | Rechazado |
| Número de vuelta inválido (`0`) | LEC, vuelta 4 | Rechazado |
| Vuelta incompleta (sin tiempo) | LEC, vuelta 9 | Rechazado |
| Código de piloto inválido (`H4M`) | HAM, vuelta 3 | Rechazado |
| Sectores incompletos (falta `s3`) | ALO, vuelta 12 | Rechazado |
| Sectores inconsistentes (+0,8 s) | RUS, vuelta 11 | Excluida de la comparación (incidencia) |
| Vueltas lentas (boxes) | ALO 1 y 8, LEC 15 | Excluidas de la comparación (incidencia) |

## Limitaciones y sesgos

- Al ser simulados, los tiempos siguen un modelo simple (ritmo base por piloto + ruido uniforme + leve degradación). No reproducen estrategias, clima ni tráfico reales.
- Los tres sectores se calculan como proporciones fijas del tiempo total (33 % / 40 % / 27 %).
- La aplicación acepta cualquier archivo con el mismo esquema, por lo que se puede reemplazar por datos reales (por ejemplo, un extracto exportado de una sesión de Fórmula 1) respetando las columnas.
