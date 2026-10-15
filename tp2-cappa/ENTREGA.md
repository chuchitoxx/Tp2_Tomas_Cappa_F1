# Checklist de entrega

## Cotejo con los siete pasos de la consigna

- [x] **1. Problema y alcance:** el README identifica problema, usuario, solución, resultados interpretables y límites de la primera versión.
- [x] **2. Datos y procedencia:** se documentan 91 observaciones, seis variables, unidad de análisis, simulación reproducible con semilla fija, responsable, condiciones de uso, fecha de generación y limitaciones. La fecha de consulta externa no aplica porque los datos son simulados.
- [x] **3. Flujo reproducible:** se leen CSV y JSON equivalentes, se valida el esquema, se registran rechazos e incidencias y se producen tablas y archivos de salida.
- [x] **4. Conceptos de programación:** hay funciones separadas por responsabilidad, la clase de dominio `Vuelta`, la abstracción `FuenteDatos` con implementaciones CSV y JSON, expresiones regulares explicadas y validaciones complementarias.
- [x] **5. Pruebas:** hay casos normales, inválidos y propiedades del resultado; comando documentado en el README. La validación más reciente ejecutó 35 pruebas; 3 pruebas de gráficos se omitieron por no estar instalado `matplotlib`.
- [x] **6. Git/GitHub:** existe `.gitignore` para entornos, cachés y salidas; el historial contiene commits de cambios concretos. Antes de entregar, confirmar que los commits locales estén publicados y que la cátedra tenga acceso al repositorio.
- [x] **7. Documentación y entrega:** están documentados instalación, comandos, organización, ejemplos, limpieza, interpretación y limitaciones. Identificar el commit evaluado al entregar; la defensa individual queda pendiente.

## Evidencia

- `README.md` del proyecto explica el problema, uso, diseño, decisiones de limpieza y limitaciones.
- `data/README.md` describe los datos, su generación y procedencia.
- `src/` contiene fuentes CSV/JSON, el modelo de dominio, la validación y el análisis.
- `tests/` contiene verificaciones ejecutables; `tests/README.md` resume su cobertura.
- `VALIDACION.md` registra los comandos y resultados de la última ejecución.

Este checklist constata evidencia en el repositorio; no sustituye la revisión del docente ni la defensa individual.
