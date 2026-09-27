# Estado · Builder_UI_3

Solo **Builder_UI_3** escribe en este archivo. Protocolo: `plan/REANUDAR.md`. Detalle de cada tarea: `plan/PLAN.md` (fase 2c).

Última actualización: 2026-09-27 12:51 CST.

## En curso

(ninguna)

## Tareas

| ID | Título | Estado | Espera |
|---|---|---|---|
| UI-23 | Rediseño de formulario, reporte y ventanas | hecha (4d7a7bd) | UI-21 (con commit y visto bueno del usuario) |
| UI-23-corrección | Foco y separación de ventanas, tabla móvil y enlace Volver | hecha (99d60c3) | UI-23 (4d7a7bd) |
| UI-23-corrección-2 | Etiqueta de desplazamiento fuera de la tabla | hecha (pendiente de commit) | UI-23-corrección (99d60c3) |

## Qué sigue

Sin tareas disponibles.

## Bitácora

- 2026-09-27 11:03 CST · UI-23 iniciada; dependencia UI-21 confirmada en `4820989` y visto bueno registrado.
- 2026-09-27 11:13 CST · UI-23 hecha (pendiente de commit). Archivos exactos: `web/estilos/formulario.css`, `web/componentes/formulario.js`, `web/componentes/confirmacion.js`, `web/componentes/duplicado.js`, `web/reporte/reporte.css`, `web/reporte/reporte.js`, `web/muestras/formulario.html`, `tests/ui/test_ui23_formularios.py`, `evidencia/UI-23/formulario-390.png`, `evidencia/UI-23/formulario-1280.png`, `evidencia/UI-23/reporte-390.png`, `evidencia/UI-23/reporte-1280.png`, `evidencia/UI-23/confirmacion-390.png`, `evidencia/UI-23/confirmacion-1280.png`, `evidencia/UI-23/duplicado-390.png`, `evidencia/UI-23/duplicado-1280.png`, `evidencia/UI-23/pendientes-390.png`, `evidencia/UI-23/pendientes-1280.png`, `plan/estado/Builder_UI_3.md`. Pruebas: UI-23 `5 passed`; suite UI `68 passed`; contraste `PASA`; suite completa `142 passed, 1 failed` por la falla ajena conocida `tests/test_int13_acceso.py::test_dos_dispositivos_y_acceso_protegido`.
- 2026-09-27 11:34 CST · UI-23 reconciliada con el commit `4d7a7bd`; UI-23-corrección iniciada por orden directa del usuario.
- 2026-09-27 11:43 CST · UI-23-corrección hecha (pendiente de commit). Archivos exactos: `web/estilos/formulario.css`, `web/reporte/reporte.css`, `tests/ui/test_ui23_formularios.py`, `evidencia/UI-23/formulario-390.png`, `evidencia/UI-23/formulario-1280.png`, `evidencia/UI-23/reporte-390.png`, `evidencia/UI-23/reporte-1280.png`, `evidencia/UI-23/confirmacion-390.png`, `evidencia/UI-23/confirmacion-1280.png`, `evidencia/UI-23/duplicado-390.png`, `evidencia/UI-23/duplicado-1280.png`, `evidencia/UI-23/pendientes-390.png`, `evidencia/UI-23/pendientes-1280.png`, `plan/estado/Builder_UI_3.md`. Las 10 capturas se regeneraron y sus 10 hashes son distintos; cuatro quedaron idénticas a su versión comprometida. Pruebas: UI-23 `5 passed`; suite completa `142 passed, 1 failed` por la falla ajena conocida `tests/test_int13_acceso.py::test_dos_dispositivos_y_acceso_protegido`; sin fallas nuevas.
- 2026-09-27 12:46 CST · UI-23-corrección reconciliada con el commit `99d60c3`; UI-23-corrección-2 iniciada por orden directa del usuario.
- 2026-09-27 12:51 CST · UI-23-corrección-2 hecha (pendiente de commit). Archivos exactos: `web/reporte/reporte.css`, `web/reporte/reporte.js`, `tests/ui/test_ui23_formularios.py`, `evidencia/UI-23/formulario-390.png`, `evidencia/UI-23/formulario-1280.png`, `evidencia/UI-23/reporte-390.png`, `evidencia/UI-23/reporte-1280.png`, `evidencia/UI-23/confirmacion-390.png`, `evidencia/UI-23/confirmacion-1280.png`, `evidencia/UI-23/duplicado-390.png`, `evidencia/UI-23/duplicado-1280.png`, `evidencia/UI-23/pendientes-390.png`, `evidencia/UI-23/pendientes-1280.png`, `plan/estado/Builder_UI_3.md`. Las 10 capturas se regeneraron y sus 10 hashes son distintos; `reporte-390.png` y `reporte-1280.png` se revisaron de cerca. Pruebas: UI-23 `5 passed`; suite completa `142 passed, 1 failed` solo por la falla ajena conocida `tests/test_int13_acceso.py::test_dos_dispositivos_y_acceso_protegido`; sin fallas nuevas.

## Observaciones

- La suite completa conserva la falla conocida de INT-13: la prueba espera actividad inmediata después de crear una oficina, pero fase 2b crea un pre-registro. UI-23 no toca ese flujo.
