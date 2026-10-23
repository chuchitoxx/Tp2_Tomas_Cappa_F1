# Checklist de entrega

## Cotejo con los siete pasos de la consigna

- [x] **1. Problema y alcance:** el README plantea el análisis del ritmo de una sesión de F1, define la finalidad y el alcance, y responde preguntas de análisis a partir de las métricas y gráficos del ejemplo.
- [x] **2. Datos y procedencia:** se documentan 91 observaciones, seis variables, unidad de análisis, simulación reproducible con semilla fija, responsable, condiciones de uso, fecha de generación y limitaciones. La fecha de consulta externa no aplica porque los datos son simulados.
- [x] **3. Flujo reproducible:** se leen CSV y JSON equivalentes, se valida el esquema, se registran rechazos e incidencias y se producen tablas y archivos de salida.
- [x] **4. Conceptos de programación:** hay funciones separadas por responsabilidad, la clase de dominio `Vuelta`, la abstracción `FuenteDatos` con implementaciones CSV y JSON, expresiones regulares explicadas y validaciones complementarias.
- [x] **5. Pruebas:** hay casos normales, inválidos y propiedades del resultado; el comando está documentado en el README y el resultado más reciente en `VALIDACION.md`.
- [x] **6. Git/GitHub:** existe `.gitignore` para entornos, cachés y salidas, y los cambios están organizados en commits concretos publicados en GitHub; confirmar que la cátedra tenga acceso.
- [x] **7. Documentación y entrega:** el README cubre el uso, el flujo, los resultados y las limitaciones; se registran el repositorio, el commit evaluado y la etiqueta de entrega.
- [ ] **Defensa individual:** preparar la exposición del trabajo.

## Evidencia

- `README.md` explica el problema, uso, diseño, decisiones de limpieza y limitaciones; además, presenta preguntas de análisis con su resolución teórica basada en los resultados del ejemplo.
- `data/README.md` describe los datos, su generación y procedencia.
- `src/` contiene fuentes CSV/JSON, el modelo de dominio, la validación y el análisis.
- `tests/` contiene verificaciones ejecutables; `tests/README.md` resume su cobertura.
- `VALIDACION.md` registra los comandos y resultados de la última ejecución.
- **Repositorio:** https://github.com/chuchitoxx/Tp2_Tomas_Cappa_F1
- **Commit de código evaluado:** `3c594b2c7e9f83f6a0d3fd08f04b1a583adefe7a`
- **Etiqueta de entrega:** `v1.0-entrega`
