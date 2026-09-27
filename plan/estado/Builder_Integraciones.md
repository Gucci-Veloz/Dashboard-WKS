# Estado · Builder_Integraciones

Solo **Builder_Integraciones** escribe en este archivo. Protocolo: `plan/REANUDAR.md`. Detalle de cada tarea: `plan/PLAN.md`.

Última actualización: 2026-09-27 · INT-07 terminada, pendiente de commit.

## En curso

(ninguna)

## Tareas

| ID | Título | Estado | Espera |
|---|---|---|---|
| INT-01 | Tabla de actividad y función de registro | hecha (0fdc1c7) | DAT-02 |
| INT-02 | API de actividad | hecha (67ac5a7) | INT-01 |
| INT-03 | Actividad sintética de Vania | hecha (d701a01) | INT-01, DAT-06 |
| INT-04 | Credencial de servicio para Vania y actor_actual | hecha (222394d) | DAT-01 |
| INT-05 | Contrato de uso para Vania | hecha (94ff4ca) | DAT-08, DAT-12, INT-02, INT-04 |
| INT-06 | Resumen de avisos agrupados | hecha (01dd661) | DAT-07 |
| INT-07 | Preferencias para reducir o silenciar avisos | hecha (pendiente de commit) | D-11, INT-06 |
| INT-08 | Mecanismo para pasar el contexto a Vania | pendiente | D-9, U-5, INT-02 |
| INT-09 | Tubería de documento imprimible | pendiente | D-7, U-3, DAT-08 |
| INT-10 | Primer documento de Works | pendiente | D-6, INT-09 |
| INT-11 | Endpoint de documentos para Vania | pendiente | D-6, D-7, INT-10 |
| INT-12 | Composición del pizarrón del mes | pendiente | D-10, DAT-13, INT-09, RES-03 |
| INT-13 | Control de acceso mínimo | hecha (f4e9d55) | D-4, INT-04 |
| INT-14 | Flujo de entrada en el teléfono | hecha (5380624) | D-4, INT-13, UI-03 |
| INT-15 | Roles Admin y Editor | cancelada (D-5: sin roles) | — |
| INT-16 | Acceso técnico del desarrollador | hecha (1f21cab) | D-4, INT-13 |
| INT-17 | Vania solo cambia datos con la sesión de quien lo pide | hecha (71b496c) | INT-13, DAT-19 |

## Qué sigue

fin de vuelta; no se inicia otra tarea.

## Observaciones

Mejoras o dudas que no se convierten en requisito. La sesión maestra las revisa.

(ninguna)

## Bitácora

Una línea por cambio, solo se agrega al final: `AAAA-MM-DD HH:MM · ID · estado · nota`.

- 2026-09-23 · — · creado · todas las tareas en pendiente
- 2026-09-23 · INT-01 · en curso · DAT-02 ya tiene commit (42a94c8), arranco tabla de actividad
- 2026-09-23 · INT-01 · hecha (0fdc1c7) · arranco INT-04
- 2026-09-23 · INT-04 · prueba OK (4 passed), autorización con encabezado `Authorization: Bearer <WORKS_TOKEN_VANIA>`
- 2026-09-23 · INT-02 · en curso · DAT-06 ya tiene commit, así que arranco INT-02 antes de INT-03
- 2026-09-23 · INT-02 · prueba OK (4 passed) · arranco INT-03
- 2026-09-23 · INT-03 · prueba OK (1 passed) · sin tareas disponibles, todas las restantes esperan D-x o U-x
- 2026-09-23 · INT-06 · en curso · works-94 corrige: D-3 ya resuelta, DAT-07 hecha; arranco INT-06
- 2026-09-23 · INT-06 · prueba OK (3 passed), hecha (01dd661) · DAT-12 aún sin commit, INT-05 sigue bloqueada; sin tareas disponibles
- 2026-09-23 · INT-05 · works-94 avisa DAT-12 hecha (4bd23f6); arranco INT-05
- 2026-09-23 · INT-05 · docs/contrato-vania.md escrito; prueba (extraer citas y compararlas contra /openapi.json) OK, 8/8 endpoints existen; documenté la diferencia de `origen_dato` entre `actividad` y las cuatro áreas, sin tocar el esquema
- 2026-09-26 · INT-15 · cancelada (D-5: sin roles) · solo el desarrollador administra cuentas mediante INT-16
- 2026-09-26 · INT-17 · pendiente · agregada con la fase 2b autorizada
- 2026-09-26 06:24 · INT-13 · en curso · D-4 resuelta e INT-04 tiene commit 222394d
- 2026-09-26 06:24 · INT-13 · bloqueada (requiere `app/actividad/registrar.py`, fuera de los archivos autorizados) · la prueba exacta deja `actividad.persona` en `null`, aunque la sesión identifica a Grecia
- 2026-09-26 06:24 · INT-17 · bloqueada (espera DAT-19: no tiene commit) · `git log --oneline --grep '^DAT-19:'` no devolvió resultados
- 2026-09-26 06:24 · INT-16 · bloqueada (espera INT-13) · INT-13 no puede cerrarse sin salir de los archivos autorizados
- 2026-09-26 06:24 · INT-14 · bloqueada (espera INT-13) · UI-03 sí tiene commit 3013e1f
- 2026-09-26 06:35 · INT-13 · en curso · corrección del plan autoriza `app/actividad/registrar.py` y los conftest; retomo el trabajo a medias
- 2026-09-26 07:30 · INT-13 · hecha (pendiente de commit) · archivos: `app/api/acceso.py`, `app/db/migraciones/005_cuentas.sql`, `app/seguridad/sesion.py`, `app/seguridad/actor.py`, `app/actividad/registrar.py`, `tests/test_int13_acceso.py`, `tests/conftest.py`, `tests/ui/conftest.py`; pruebas: 5 + 61 + 41 passed
- 2026-09-26 07:32 · INT-13 · hecha (f4e9d55) · commit detectado; INT-16 en curso
- 2026-09-26 07:32 · INT-16 · bloqueada (registrar teléfonos fuera de git requiere que `app/seguridad/sesion.py` lea esa configuración, archivo fuera de los autorizados) · no se modificaron archivos de la tarea
- 2026-09-26 08:00 · INT-16 · hecha (490d305) · commit detectado; arranco INT-14
- 2026-09-26 08:00 · INT-14 · en curso · D-4, INT-13 y UI-03 tienen commit; arranco flujo de entrada
- 2026-09-26 08:00 · INT-14 · hecha (pendiente de commit) · archivos: `web/acceso/index.html`, `web/acceso/acceso.css`, `web/acceso/acceso.js`, `tests/ui/test_int14_entrada.py`, `evidencia/INT-14/entrada-390.png`, `plan/estado/Builder_Integraciones.md`; prueba: `.venv/bin/python -m pytest tests/ui/test_int14_entrada.py -q` OK (2 passed)
- 2026-09-26 08:00 · INT-16 · en curso · el usuario autoriza `app/seguridad/sesion.py`; retomo la tarea previamente bloqueada
- 2026-09-26 08:00 · INT-16 · hecha (pendiente de commit) · archivos: `app/seguridad/admin.py`, `app/seguridad/sesion.py`, `tests/test_int16_admin.py`, `plan/estado/Builder_Integraciones.md`; prueba: `.venv/bin/python -m pytest tests/test_int16_admin.py -q` OK (3 passed)
- 2026-09-26 08:41 · INT-14 · hecha (5380624) · commit detectado
- 2026-09-26 08:41 · INT-16 · hecha (1f21cab) · commit detectado
- 2026-09-26 08:41 · INT-17 · en curso · INT-13 y DAT-19 tienen commit; arranco la tarea
- 2026-09-26 08:41 · INT-17 · hecha (pendiente de commit) · archivos: `app/seguridad/actor.py`, `app/seguridad/vania.py`, `docs/contrato-vania.md`, `tests/test_int17_vania_sesion.py`, `plan/estado/Builder_Integraciones.md`; prueba: `.venv/bin/python -m pytest tests/test_int17_vania_sesion.py -q` OK (4 passed)
- 2026-09-27 13:09 · INT-17 · hecha (71b496c) · commit detectado
- 2026-09-27 13:09 · INT-07 · en curso · D-11 resuelta como A + (i) e INT-06 tiene commit 01dd661
- 2026-09-27 13:17 · INT-07 · hecha (pendiente de commit) · archivos: `app/db/migraciones/003_preferencias_avisos.sql`, `app/api/avisos.py`, `tests/test_int07_preferencias.py`, `plan/estado/Builder_Integraciones.md`; pruebas: `.venv/bin/python -m pytest tests/test_int07_preferencias.py -q` OK (6 passed), `tests/test_int06_avisos.py` dentro de la corrida conjunta OK (3 passed), suite completa 148 passed y 1 falla preexistente en `tests/test_int13_acceso.py::test_dos_dispositivos_y_acceso_protegido`, reproducida también en una copia limpia de HEAD
