# Pruebas

Las pruebas usan `unittest` (biblioteca estándar). Se ejecutan desde la **raíz del repositorio**:

```bash
python -m unittest discover -s tests -v
```

## Qué se verifica

| Requisito | Pruebas |
|---|---|
| Caso normal | `test_caso_normal_dos_formatos`, `test_caso_normal_estadisticos`, `test_caso_normal_sin_rechazos` |
| Entrada inválida / caso límite | `test_entradas_invalidas`, `test_rechazos_con_motivo`, `test_esquema_sin_columna_obligatoria`, `test_piloto_inexistente`, `test_una_sola_vuelta_valida`, `test_piloto_sin_vueltas_utilizables`, `test_json_invalido`, `test_archivo_inexistente` |
| Propiedad del resultado | `test_equivalencia_csv_json` (CSV y JSON se leen igual), `test_conservacion_de_registros` (válidos + rechazados = leídos), `test_propiedades_del_resultado` (mejor ≤ media ≤ peor, desvío ≥ 0), `test_reproducibilidad_y_equivalencia` (mismas entradas, mismas salidas) |
| Tolerancia de sectores y vueltas lentas | `test_tolerancia_de_sectores`, `test_vuelta_lenta_excluida` |
| Sectores y vuelta ideal | `test_caso_normal_vuelta_ideal`, `test_piloto_sin_sectores`, `test_vuelta_ideal_no_supera_la_mejor_vuelta` |
| Gráficos (se omiten sin matplotlib) | `test_se_generan_los_cuatro_graficos`, `test_un_solo_piloto_no_rompe`, `test_sin_graficos_no_crea_png` |
| Jerarquía de fuentes | `test_jerarquia`, `test_fuente_para_por_extension` |

Resultado esperado: `Ran 34 tests ... OK`. Los tests de gráficos requieren `pip install -r requirements.txt`; si matplotlib no está, se omiten (`skipped`).
