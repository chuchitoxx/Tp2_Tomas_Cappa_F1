"""Pruebas de los gráficos (se omiten si matplotlib no está instalado)."""

import os
import sys
import tempfile
import unittest

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(RAIZ, "src"))

import main as app  # noqa: E402

try:
    import matplotlib  # noqa: F401

    HAY_MATPLOTLIB = True
except ImportError:
    HAY_MATPLOTLIB = False

CSV_PRUEBA = os.path.join(RAIZ, "data", "sesion_f1.csv")
ESPERADOS = [
    "grafico_mejor_vuelta.png",
    "grafico_evolucion_vueltas.png",
    "grafico_dispersion.png",
    "grafico_sectores.png",
]


@unittest.skipUnless(HAY_MATPLOTLIB, "matplotlib no está instalado")
class TestGraficos(unittest.TestCase):
    def test_se_generan_los_cuatro_graficos(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(app.main(["--entrada", CSV_PRUEBA, "--salida", tmp]), 0)
            for nombre in ESPERADOS:
                ruta = os.path.join(tmp, nombre)
                self.assertTrue(os.path.isfile(ruta), nombre)
                self.assertGreater(os.path.getsize(ruta), 5000, nombre)

    def test_un_solo_piloto_no_rompe(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                app.main(
                    ["--entrada", CSV_PRUEBA, "--salida", tmp, "--pilotos", "VER"]
                ),
                0,
            )
            self.assertTrue(os.path.isfile(os.path.join(tmp, "grafico_dispersion.png")))

    def test_sin_graficos_no_crea_png(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(
                app.main(["--entrada", CSV_PRUEBA, "--salida", tmp, "--sin-graficos"]),
                0,
            )
            self.assertFalse(any(n.endswith(".png") for n in os.listdir(tmp)))


if __name__ == "__main__":
    unittest.main()
