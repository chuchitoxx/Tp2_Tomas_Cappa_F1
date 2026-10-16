"""Pruebas del comparador de vueltas.

Ejecutar desde la raíz del repositorio:
    python -m unittest discover -s tests -v
"""

import os
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(RAIZ, "src"))

import main as app  # noqa: E402
from fuentes import FuenteCSV, FuenteDatos, FuenteJSON, fuente_para  # noqa: E402
from modelos import Vuelta  # noqa: E402
from pipeline import (
    EsquemaInvalidoError,
    ResultadoInconsistenteError,  # noqa: E402
    comparar_pilotos,
    comparar_sectores,
    convertir_tiempo,
    limpiar_datos,
    normalizar_campos,
    segundos_a_texto,
    seleccionar_vueltas,
    validar_esquema,
    verificar_resultado,
)

CSV_PRUEBA = os.path.join(RAIZ, "data", "sesion_f1.csv")
JSON_PRUEBA = os.path.join(RAIZ, "data", "sesion_f1.json")


def fila(piloto, vuelta, tiempo, s1="", s2="", s3=""):
    return {
        "piloto": piloto,
        "vuelta": str(vuelta),
        "tiempo": tiempo,
        "s1": s1,
        "s2": s2,
        "s3": s3,
    }


def preparar(filas):
    return limpiar_datos(normalizar_campos(filas))


class TestConversionTiempo(unittest.TestCase):
    def test_caso_normal_dos_formatos(self):
        self.assertAlmostEqual(convertir_tiempo("1:25.123"), 85.123)
        self.assertAlmostEqual(convertir_tiempo("85.123"), 85.123)

    def test_ida_y_vuelta(self):
        self.assertEqual(segundos_a_texto(convertir_tiempo("1:05.500")), "1:05.500")

    def test_entradas_invalidas(self):
        for malo in ("", "abc", "1:2x.456", "1:75.000", "1:25", None):
            with self.subTest(valor=malo):
                with self.assertRaises(ValueError):
                    convertir_tiempo(malo)


class TestLimpieza(unittest.TestCase):
    def test_caso_normal_sin_rechazos(self):
        vueltas, rechazos = preparar(
            [fila("VER", 1, "1:25.000"), fila("VER", 2, "1:26.000")]
        )
        self.assertEqual(len(vueltas), 2)
        self.assertEqual(rechazos, [])

    def test_piloto_minuscula_se_normaliza(self):
        vueltas, _ = preparar([fila("ver", 1, "1:25.000")])
        self.assertEqual(vueltas[0].piloto, "VER")

    def test_numero_de_vuelta_decimal_no_entero_se_rechaza(self):
        vueltas, rechazos = preparar([fila("VER", "2.5", "1:25.000")])
        self.assertEqual(vueltas, [])
        self.assertIn("número de vuelta inválido", rechazos[0]["motivo"])

    def test_numero_de_vuelta_excesivo_se_rechaza(self):
        vueltas, rechazos = preparar([fila("VER", "1e999999999", "1:25.000")])
        self.assertEqual(vueltas, [])
        self.assertEqual(len(rechazos), 1)

    def test_rechazos_con_motivo(self):
        filas = [
            fila("H4M", 1, "1:25.000"),  # piloto inválido
            fila("VER", 0, "1:25.000"),  # vuelta inválida
            fila("VER", 2, ""),  # incompleta
            fila("VER", 3, "xx"),  # formato
            fila("VER", 4, "0:10.000"),  # fuera de rango
            fila("VER", 5, "1:25.000", "28.0", "34.0", ""),  # sectores incompletos
            fila("VER", 6, "1:25.000"),  # válida
            fila("VER", 6, "1:25.500"),  # duplicada
        ]
        vueltas, rechazos = preparar(filas)
        self.assertEqual(len(vueltas), 1)
        self.assertEqual(len(rechazos), 7)
        self.assertTrue(all(r["motivo"] for r in rechazos))

    def test_conservacion_de_registros(self):
        """Propiedad: válidos + rechazados == registros leídos."""
        filas = FuenteCSV().cargar(CSV_PRUEBA)
        vueltas, rechazos = preparar(filas)
        self.assertEqual(len(vueltas) + len(rechazos), len(filas))

    def test_esquema_sin_columna_obligatoria(self):
        filas = normalizar_campos([{"piloto": "VER", "vuelta": "1"}])
        with self.assertRaises(EsquemaInvalidoError) as ctx:
            validar_esquema(filas)
        self.assertIn("tiempo", str(ctx.exception))

    def test_esquema_vacio(self):
        with self.assertRaises(EsquemaInvalidoError):
            validar_esquema([])


class TestVuelta(unittest.TestCase):
    def test_diferencia_de_sectores(self):
        v = Vuelta("VER", 1, 86.0, [28.0, 34.0, 23.0])
        self.assertAlmostEqual(v.suma_sectores(), 85.0)
        self.assertAlmostEqual(v.diferencia_sectores(), 1.0)
        self.assertFalse(v.es_consistente(0.5))
        self.assertTrue(v.es_consistente(1.0))

    def test_sin_sectores_es_consistente(self):
        v = Vuelta("VER", 1, 86.0)
        self.assertIsNone(v.diferencia_sectores())
        self.assertTrue(v.es_consistente(0.0))


class TestSeleccionYComparacion(unittest.TestCase):
    def setUp(self):
        self.vueltas = [
            Vuelta("VER", 1, 85.0),
            Vuelta("VER", 2, 86.0),
            Vuelta("VER", 3, 87.0),
            Vuelta("NOR", 1, 90.0),
        ]

    def test_caso_normal_estadisticos(self):
        sel, inc = seleccionar_vueltas(self.vueltas, ["VER"])
        res = comparar_pilotos(sel, ["VER"])
        self.assertEqual(inc, [])
        self.assertEqual(res[0]["mejor_s"], 85.0)
        self.assertEqual(res[0]["media_s"], 86.0)
        self.assertEqual(res[0]["desvio_s"], 1.0)
        self.assertEqual(res[0]["vueltas_usadas"], "1 2 3")

    def test_una_sola_vuelta_valida(self):
        sel, _ = seleccionar_vueltas(self.vueltas, ["NOR"])
        res = comparar_pilotos(sel, ["NOR"])
        self.assertEqual(res[0]["n_vueltas"], 1)
        self.assertIsNone(res[0]["desvio_s"])
        self.assertIn("dispersión no definida", res[0]["nota"])

    def test_piloto_sin_vueltas_utilizables(self):
        res = comparar_pilotos([], ["VER"])
        self.assertEqual(res[0]["n_vueltas"], 0)
        self.assertIsNone(res[0]["mejor_s"])
        self.assertIn("sin vueltas", res[0]["nota"])

    def test_piloto_inexistente(self):
        with self.assertRaises(ValueError) as ctx:
            seleccionar_vueltas(self.vueltas, ["XXX"])
        self.assertIn("Pilotos disponibles", str(ctx.exception))

    def test_codigo_de_piloto_invalido(self):
        with self.assertRaises(ValueError):
            seleccionar_vueltas(self.vueltas, ["V3R"])

    def test_tolerancia_de_sectores(self):
        v = [
            Vuelta("VER", 1, 86.0, [28.0, 34.0, 23.0]),
            Vuelta("VER", 2, 85.0, [28.0, 34.0, 23.0]),
        ]
        sel, inc = seleccionar_vueltas(v, ["VER"], tolerancia=0.5)
        self.assertEqual([x.numero for x in sel], [2])
        self.assertEqual(inc[0]["tipo"], "sectores inconsistentes")
        sel, inc = seleccionar_vueltas(v, ["VER"], tolerancia=1.0)  # ahora se acepta
        self.assertEqual(len(sel), 2)
        self.assertEqual(inc, [])

    def test_vuelta_lenta_excluida(self):
        v = [
            Vuelta("VER", 1, 85.0),
            Vuelta("VER", 2, 86.0),
            Vuelta("VER", 3, 85.5),
            Vuelta("VER", 4, 120.0),
        ]
        sel, inc = seleccionar_vueltas(v, ["VER"])
        self.assertEqual([x.numero for x in sel], [1, 2, 3])
        self.assertEqual(inc[0]["tipo"], "vuelta lenta")

    def test_propiedades_del_resultado(self):
        """Propiedad: mejor <= media <= peor y desvío >= 0 para cada piloto."""
        vueltas, _ = preparar(FuenteCSV().cargar(CSV_PRUEBA))
        sel, _ = seleccionar_vueltas(vueltas)
        pilotos = sorted({v.piloto for v in vueltas})
        res = comparar_pilotos(sel, pilotos)
        verificar_resultado(res, sel)
        for f in res:
            tiempos = [v.tiempo_s for v in sel if v.piloto == f["piloto"]]
            self.assertLessEqual(f["mejor_s"], f["media_s"])
            self.assertLessEqual(f["media_s"], max(tiempos))
            self.assertGreaterEqual(f["desvio_s"], 0)

    def test_verificar_detecta_resultado_incoherente(self):
        sel = [Vuelta("VER", 1, 85.0)]
        res = comparar_pilotos(sel, ["VER"])
        res[0]["n_vueltas"] = 5
        with self.assertRaises(ResultadoInconsistenteError):
            verificar_resultado(res, sel)


class TestSectores(unittest.TestCase):
    def test_caso_normal_vuelta_ideal(self):
        v = [
            Vuelta("VER", 1, 85.0, [28.0, 34.0, 23.0]),
            Vuelta("VER", 2, 85.1, [27.9, 34.2, 23.0]),
        ]
        res = comparar_sectores(v, ["VER"])[0]
        self.assertEqual(
            (res["mejor_s1"], res["mejor_s2"], res["mejor_s3"]), (27.9, 34.0, 23.0)
        )
        self.assertAlmostEqual(res["vuelta_ideal_s"], 84.9)

    def test_piloto_sin_sectores(self):
        res = comparar_sectores([Vuelta("VER", 1, 85.0)], ["VER"])[0]
        self.assertEqual(res["n_vueltas_con_sectores"], 0)
        self.assertIsNone(res["vuelta_ideal_s"])

    def test_vuelta_ideal_no_supera_la_mejor_vuelta(self):
        """Propiedad: la vuelta ideal <= mejor vuelta (más la tolerancia de sectores)."""
        vueltas, _ = preparar(FuenteCSV().cargar(CSV_PRUEBA))
        sel, _ = seleccionar_vueltas(vueltas, tolerancia=0.05)
        pilotos = sorted({v.piloto for v in vueltas})
        mejores = {f["piloto"]: f["mejor_s"] for f in comparar_pilotos(sel, pilotos)}
        for f in comparar_sectores(sel, pilotos):
            self.assertLessEqual(f["vuelta_ideal_s"], mejores[f["piloto"]] + 0.05)


class TestFuentes(unittest.TestCase):
    def test_jerarquia(self):
        self.assertTrue(issubclass(FuenteCSV, FuenteDatos))
        self.assertTrue(issubclass(FuenteJSON, FuenteDatos))
        with self.assertRaises(TypeError):
            FuenteDatos()  # clase abstracta: no se instancia

    def test_equivalencia_csv_json(self):
        """Propiedad: CSV y JSON equivalentes se leen igual."""
        self.assertEqual(
            FuenteCSV().cargar(CSV_PRUEBA), FuenteJSON().cargar(JSON_PRUEBA)
        )

    def test_json_acepta_numero_de_vuelta_decimal_entero(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "vuelta_decimal.json")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write('[{"piloto":"VER","vuelta":2.0,"tiempo":"1:25.000"}]')

            vueltas, rechazos = preparar(FuenteJSON().cargar(ruta))

        self.assertEqual([v.numero for v in vueltas], [2])
        self.assertEqual(rechazos, [])

    def test_csv_recorta_espacios_en_encabezados(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "espacios.csv")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write(" piloto, vuelta, tiempo \nVER,1,1:24.675\n")

            self.assertEqual(
                FuenteCSV().cargar(ruta),
                [{"piloto": "VER", "vuelta": "1", "tiempo": "1:24.675"}],
            )

    def test_fuente_para_por_extension(self):
        self.assertIsInstance(fuente_para("a.csv"), FuenteCSV)
        self.assertIsInstance(fuente_para("a.JSON"), FuenteJSON)
        with self.assertRaises(ValueError):
            fuente_para("a.xlsx")

    def test_archivo_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            FuenteCSV().cargar("no_existe.csv")

    def test_json_invalido(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "malo.json")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write("{esto no es json")
            with self.assertRaises(ValueError):
                FuenteJSON().cargar(ruta)

    def test_json_con_estructura_incorrecta(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = os.path.join(tmp, "raro.json")
            with open(ruta, "w", encoding="utf-8") as f:
                f.write('"solo un texto"')
            with self.assertRaises(ValueError):
                FuenteJSON().cargar(ruta)


class TestAplicacion(unittest.TestCase):
    def _ejecutar(self, entrada, salida, extra=()):
        return app.main(
            ["--entrada", entrada, "--salida", salida, "--sin-graficos", *extra]
        )

    def _leer(self, carpeta):
        with open(
            os.path.join(carpeta, "comparacion_pilotos.csv"), encoding="utf-8"
        ) as f:
            return f.read()

    def test_reproducibilidad_y_equivalencia(self):
        """Mismas entradas -> mismo resultado; CSV y JSON dan el mismo reporte."""
        with tempfile.TemporaryDirectory() as tmp:
            a, b, c = (os.path.join(tmp, x) for x in "abc")
            for entrada, salida in ((CSV_PRUEBA, a), (CSV_PRUEBA, b), (JSON_PRUEBA, c)):
                self.assertEqual(self._ejecutar(entrada, salida), 0)
            self.assertEqual(self._leer(a), self._leer(b))
            self.assertEqual(self._leer(a), self._leer(c))

    def test_errores_devuelven_codigo_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(self._ejecutar("no_existe.csv", tmp), 1)
            self.assertEqual(self._ejecutar(CSV_PRUEBA, tmp, ["--pilotos", "ZZZ"]), 1)
            self.assertEqual(self._ejecutar(CSV_PRUEBA, tmp, ["--tolerancia", "-1"]), 1)


if __name__ == "__main__":
    unittest.main()
