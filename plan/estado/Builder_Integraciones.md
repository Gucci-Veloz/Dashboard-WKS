# Estado · Builder_Integraciones

Solo **Builder_Integraciones** escribe en este archivo. Protocolo: `plan/REANUDAR.md`. Detalle de cada tarea: `plan/PLAN.md`.

Última actualización: 2026-09-23 · creado por el planificador (Mapping). Plan aprobado el 2026-09-23; D-1, D-2 y D-3 resueltas.

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
| INT-07 | Preferencias para reducir o silenciar avisos | pendiente | D-11, INT-06 |
| INT-08 | Mecanismo para pasar el contexto a Vania | pendiente | D-9, U-5, INT-02 |
| INT-09 | Tubería de documento imprimible | pendiente | D-7, U-3, DAT-08 |
| INT-10 | Primer documento de Works | pendiente | D-6, INT-09 |
| INT-11 | Endpoint de documentos para Vania | pendiente | D-6, D-7, INT-10 |
| INT-12 | Composición del pizarrón del mes | pendiente | D-10, DAT-13, INT-09, RES-03 |
| INT-13 | Control de acceso mínimo | pendiente | D-4, INT-04 |
| INT-14 | Flujo de entrada en el teléfono | pendiente | D-4, INT-13, UI-03 |
| INT-15 | Roles Admin y Editor | pendiente | D-5, INT-14 |
| INT-16 | Acceso técnico del desarrollador | pendiente | D-4, INT-13 |

## Qué sigue

DAT-12 ya tiene commit (4bd23f6): INT-05 hecha. Sin tareas disponibles: espero D-11 (INT-07), D-9/U-5 (INT-08), D-6/D-7/U-3 (INT-09 a INT-11), D-10 (INT-12) y D-4/D-5 (INT-13 a INT-16).

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
