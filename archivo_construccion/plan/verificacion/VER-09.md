# VER-09 · Verificación de la fase 2b

Fecha: 2026-09-26.

## Resultado de pruebas

- `.venv/bin/python -m pytest tests/test_dat18_cambios.py tests/test_dat19_api_cambios.py tests/test_dat09_oficinas.py tests/test_dat10_*.py tests/test_dat11_*.py tests/test_dat12_*.py tests/test_dat20_duplicados.py tests/test_dat21_reporte.py tests/test_dat22_descartar.py tests/test_int17_vania_sesion.py tests/ui/test_ui09_formulario.py tests/ui/test_ui10_*.py tests/ui/test_ui11_*.py tests/ui/test_ui12_*.py tests/ui/test_ui13_*.py tests/ui/test_ui18_confirmar.py tests/ui/test_ui20_reporte.py -q`: **FALLA**, 45 pasaron y 1 falló. `test_reporte_abre_hoy_muestra_columnas_y_no_contamina_nivel1` navega a `#reporte` y después espera que `#app` no tenga tabla; se observó 1 tabla.
- `.venv/bin/python -m pytest tests/test_int13_acceso.py -q`: **FALLA**, 4 pasaron y 1 falló. `test_dos_dispositivos_y_acceso_protegido` recibió una lista vacía en `/api/actividad` y falló al consultar `actividad[0]`.
- `.venv/bin/python -m pytest -q`: **FALLA**, 121 pasaron y 2 fallaron en 49.46 s: las dos fallas anteriores.
- `.venv/bin/python -m pytest tests/test_int13_acceso.py::test_sesion_vence_a_las_horas_indicadas tests/test_dat18_cambios.py::test_pendiente_vencido_desaparece_y_no_se_confirma tests/test_dat18_cambios.py::test_vania_no_puede_ser_solicitante tests/test_dat21_reporte.py::test_reporte_solo_muestra_confirmados_del_dia -q`: **PASA**, 4 pruebas.

## Revisión contra las reglas de operación

- **Confirmación antes del dato oficial: PASA.** `/openapi.json` expone 16 rutas `POST`/`PUT`/`DELETE`. Las doce rutas de las cuatro áreas y `POST /api/pagos/registrar` pasan por `crear_pendiente`; solo `POST /api/cambios/{cambio_id}/confirmar` llama a `confirmar`. Las pruebas DAT-19 incluidas en la corrida verificaron alta, modificación, baja y registro de pago antes y después de confirmar.
- **Vania no es solicitante: PASA.** La prueba focalizada de DAT-18 rechaza `solicitante='vania'`; la prueba de INT-17 incluida en la corrida pasó y comprueba `solicitante=grecia, ejecutor=vania`.
- **Pendiente vencido: PASA.** La prueba focalizada de DAT-18 pasó: el vencido no se confirma y desaparece.
- **Reporte: PASA en API.** La prueba focalizada de DAT-21 pasó: el pendiente no aparece. La interfaz de UI-20 tiene la falla descrita arriba.
- **Vencimiento de sesión: PASA.** La prueba focalizada de INT-13 pasó para 18:00 y para 23:59 cuando la sesión se crea después de las 18:00.
- **Solo `app/db/` abre SQLite: PASA.** `grep -rn "sqlite3" app --include='*.py' | grep -v '^app/db/'` no produjo salida.
- **Números de teléfono en git: FALLA literal del comando.** `git grep -nE "\\+?52 ?1? ?[0-9]{2,3} ?[0-9]{3,4} ?[0-9]{4}"` devolvió 18 coincidencias, todas en pruebas y con números ficticios `+520000000001` a `+520000000004`; no se observó un número real.

## Conclusión

La verificación está completa. Permanecen dos fallas de prueba: la histórica de `test_dos_dispositivos_y_acceso_protegido` y la de UI-20. El criterio literal de ausencia de números tampoco pasa porque los números ficticios de prueba coinciden con el patrón indicado.
