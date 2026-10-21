# Reproducibilidad

Esta guía permite preparar el entorno y repetir el procesamiento del conjunto de prueba. Requiere **Python 3.9 o superior**. El análisis y las pruebas usan la biblioteca estándar; `matplotlib` se necesita para generar gráficos y ejecutar sus pruebas.

## Preparar el entorno

### Linux

```bash
git clone https://github.com/chuchitoxx/Tp2_Tomas_Cappa_F1.git
cd Tp2_Tomas_Cappa_F1

python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Si no está disponible `venv`, instalá el paquete de entornos virtuales de Python de tu distribución (por ejemplo, `python3-venv` en Debian o Ubuntu) y repetí la creación del entorno.

### Windows (PowerShell)

```powershell
git clone https://github.com/chuchitoxx/Tp2_Tomas_Cappa_F1.git
cd Tp2_Tomas_Cappa_F1

py -3 --version
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Si PowerShell impide activar el entorno, no hace falta cambiar la política de ejecución: usá `.\.venv\Scripts\python.exe` en lugar de `python` en los comandos siguientes.

La instalación de `requirements.txt` agrega `matplotlib`; se puede omitir si sólo se quieren procesar datos y correr pruebas sin gráficos.

## Ejecutar el conjunto de prueba

Desde la raíz del repositorio, el siguiente comando funciona aunque `matplotlib` no esté instalado:

```bash
python src/main.py --entrada data/sesion_f1.csv --sin-graficos
```

Para generar los gráficos, quitá `--sin-graficos`:

```bash
python src/main.py --entrada data/sesion_f1.csv
python src/main.py --entrada data/sesion_f1.json
python src/main.py --entrada data/sesion_f1.csv --pilotos VER NOR LEC --tolerancia 0.1
```

Con el CSV de prueba, la ejecución debe terminar con código `0` e informar **91 registros leídos, 84 válidos, 7 rechazados, 4 vueltas excluidas y 80 utilizadas**. La tabla debe mostrar a VER con la vuelta más rápida (`1:24.675`) y a LEC con el menor desvío (`0.219 s`). Los reportes y gráficos se guardan en `outputs/`.

## Comparar CSV y JSON

Generá los dos reportes desde la raíz del repositorio:

```bash
python src/main.py --entrada data/sesion_f1.csv --salida outputs/reporte-csv --sin-graficos
python src/main.py --entrada data/sesion_f1.json --salida outputs/reporte-json --sin-graficos
```

En Linux, comparalos con:

```bash
diff -u outputs/reporte-csv/comparacion_pilotos.csv outputs/reporte-json/comparacion_pilotos.csv
```

En Windows PowerShell:

```powershell
Compare-Object (Get-Content outputs/reporte-csv/comparacion_pilotos.csv) (Get-Content outputs/reporte-json/comparacion_pilotos.csv)
```

Si no se muestra ninguna diferencia, ambos formatos produjeron el mismo reporte. El argumento `--salida` permite elegir otra carpeta de salida.

## Ejecutar las pruebas automatizadas

La suite comprueba lectura CSV/JSON, conversiones, validaciones, limpieza, métricas, salidas y gráficos. Algunos casos cargan el conjunto de prueba de `data/`. Desde la raíz y con el entorno virtual activo, ejecutá:

```bash
python -m unittest discover -s tests -v
```

Si todo está correcto, el comando termina con `OK` y código de salida `0`. La última verificación registró 39 pruebas aprobadas; el detalle está en [VALIDACION.md](VALIDACION.md). Las pruebas de gráficos se omiten si `matplotlib` no está instalado.

Para volver a generar el conjunto de prueba simulado (opcional), ejecutá `python scripts/generar_datos.py`; la semilla fija reproduce los mismos archivos.