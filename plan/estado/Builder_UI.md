# Estado · Builder_UI

Solo **Builder_UI** escribe en este archivo. Protocolo: `plan/REANUDAR.md`. Detalle de cada tarea: `plan/PLAN.md`.

Última actualización: 2026-09-23 · Builder_UI, UI-02 hecha.

## En curso

(ninguna)

## Tareas

| ID | Título | Estado | Espera |
|---|---|---|---|
| UI-01 | Página base mobile-first | hecha | D-1, DAT-01, UI-02 |
| UI-02 | Tokens de diseño y verificador de contraste | hecha | — (libre) |
| UI-03 | Componentes neumórficos base | hecha | D-1, UI-01 |
| UI-04 | Nivel 1: estado general con ejemplos del contrato | hecha | UI-03, DAT-03 |
| UI-05 | Nivel 2: lo que merece atención | hecha | UI-04 |
| UI-06 | Indicadores que explican el estado | hecha | UI-05 |
| UI-07 | Conectar niveles 1 y 2 al servicio | hecha | DAT-08 (D-3), UI-06 |
| UI-08 | Entrada al detalle bajo demanda | hecha | UI-05 |
| UI-09 | Formulario editable y confirmación visible | hecha | UI-03 |
| UI-10 | Detalle de oficinas | hecha | DAT-09, UI-08, UI-09 |
| UI-11 | Detalle de inquilinos | hecha | DAT-10, UI-10 |
| UI-12 | Detalle de contratos | hecha | DAT-11, UI-11 |
| UI-13 | Detalle de pagos y registrar pago | hecha | DAT-12, UI-12 |
| UI-14 | Rastro de Vania visible | pendiente | D-8, INT-02, INT-03, UI-07 |
| UI-15 | Botón seguir con Vania | pendiente | INT-08, UI-13 |
| UI-16 | Ajustar el detalle a los campos reales | pendiente | DAT-15, UI-13 |
| UI-17 | Efecto de sorpresa por calidad | pendiente | D-15, UI-07 |
| UI-18 | Ventana de confirmación y cambios pendientes | bloqueada (falta API para descartar un pendiente) | DAT-19, INT-14 |
| UI-19 | Aviso de posible duplicado | pendiente | DAT-20, UI-18 |
| UI-20 | Botón y pantalla "Reporte del día" | pendiente | DAT-21, UI-18 |

## Qué sigue

sin tareas disponibles: UI-18 bloqueada (falta API para descartar un pendiente); UI-19 espera DAT-20 y UI-20 espera DAT-21; UI-15 espera INT-08, UI-16 espera DAT-15, y UI-14/UI-17 esperan D-8/D-15 del usuario.

## Observaciones

Mejoras o dudas que no se convierten en requisito. La sesión maestra las revisa.

(ninguna)

## Bitácora

Una línea por cambio, solo se agrega al final: `AAAA-MM-DD HH:MM · ID · estado · nota`.

- 2026-09-23 · — · creado · todas las tareas en pendiente
- 2026-09-23 05:00 · UI-02 · en curso · tokens de diseño y verificador de contraste
- 2026-09-23 05:10 · UI-02 · hecha (c4a62ee) · sin tareas disponibles, espero DAT-01
- 2026-09-23 05:20 · UI-01 · en curso · DAT-01 hecha (aaf12f0), empiezo página base
- 2026-09-23 05:35 · UI-01 · hecha (8c226f0) · sigue UI-03
- 2026-09-23 05:36 · UI-03 · en curso · componentes neumórficos base
- 2026-09-23 05:55 · UI-03 · hecha (3013e1f) · corregí un bug en web/estilos/tokens.css (UI-02): el comentario de cabecera tenía un `*/` literal dentro del texto que cerraba el comentario antes de tiempo y rompía el parseo de todo el archivo (0 reglas CSS cargadas en el navegador). Sin este arreglo ningún estilo de tokens.css se aplicaba. Sigue UI-04 o UI-09.
- 2026-09-23 05:56 · UI-04 · en curso · nivel 1 con conclusión humana
- 2026-09-23 06:10 · UI-04 · hecha (2b7c804) · corregí una prueba con carrera (UI-03): test_boton_presionado_cambia_borde_o_color leía el estilo computado antes de que terminara la transición CSS de 0.12s, y fallaba de forma intermitente al correr junto con otras pruebas. Agregué una espera corta. Sigue UI-05 o UI-09.
- 2026-09-23 06:12 · UI-05 · en curso · nivel 2 con asuntos en lenguaje humano
- 2026-09-23 06:25 · UI-05 · hecha (3f5aa67) · sigue UI-06, UI-08 o UI-09
- 2026-09-23 06:26 · UI-06 · en curso · indicadores textuales
- 2026-09-23 06:40 · UI-06 · hecha (0ba8a1b) · ajusté las pruebas de UI-04 y UI-05, que asumían "ninguna lista" como ningún `ul`/`ol` en toda la página; con los indicadores (que sí son una lista y se muestran siempre) esa aserción era demasiado amplia. Las dejé apuntando a lo que de verdad importaba: que no aparezca la lista de asuntos. app/fuentes/cargar.py falló en la corrida completa, pero es de Builder_Datos y no lo toqué. Sigue UI-08 o UI-09; UI-07 sigue esperando DAT-08.
- 2026-09-23 06:41 · UI-08 · en curso · navegación por hash, conecté app.js e index.html (UI-01) a los módulos existentes
- 2026-09-23 06:58 · UI-08 · hecha (c2b5ee3) · sigue UI-09; UI-07 sigue esperando DAT-08
- 2026-09-23 06:59 · UI-07 · en curso · DAT-08 hecha (fac977b), conecto niveles 1 y 2 a /api/estado
- 2026-09-23 07:20 · UI-07 · hecha (39762f4) · sembré la base de pruebas de UI con el escenario con_atencion en tests/ui/conftest.py, para que la app real (no solo las muestras) tenga datos. Sigue UI-09.
- 2026-09-23 07:21 · UI-09 · en curso · formulario editable y confirmación de guardado
- 2026-09-23 07:35 · UI-09 · hecha (65efdc9) · sin tareas disponibles: espero DAT-09 a DAT-12 (UI-10 a UI-13) y D-8/D-15 del usuario (UI-14, UI-17)
- 2026-09-23 07:45 · UI-10 · en curso · DAT-09 a DAT-12 hechas (hasta 4bd23f6, avisó works-94); detalle de oficinas
- 2026-09-23 08:05 · UI-10 · hecha (b36510c) · extendí web/navegacion/rutas.js para soportar `#area` (lista) además de `#tipo-id` (ficha), sin tocar el mapeo fijo de áreas; corregí un bug real en app.js (UI-08): renderRegistro no esperaba (`await`) a que renderDetalle terminara antes de agregar "Volver", y como el módulo de detalle limpia su propio contenedor de forma asíncrona, podía borrar el botón recién agregado. Sigue UI-11.
- 2026-09-23 08:06 · UI-11 · en curso · detalle de inquilinos, mismo patrón que UI-10
- 2026-09-23 08:18 · UI-11 · hecha (04903e4) · sigue UI-12
- 2026-09-23 08:19 · UI-12 · en curso · detalle de contratos, con fecha de fin en forma humana
- 2026-09-23 08:35 · UI-12 · hecha (ceeda51) · sigue UI-13
- 2026-09-23 08:36 · UI-13 · en curso · detalle de pagos y registrar pago
- 2026-09-23 08:55 · UI-13 · hecha · corregí un bug propio: al registrar el pago, borraba de inmediato el contenedor de la acción (`zonaAccion.innerHTML = ""`) antes de que formulario.js alcanzara a mostrar la confirmación, así que la confirmación quedaba en un nodo ya desprendido del DOM y nunca se veía. Ahora solo actualizo los campos de la edición general en vivo, sin destruir el formulario de acción. Sin tareas disponibles: espero INT-08 (UI-15) y DAT-15 (UI-16); UI-14 y UI-17 esperan D-8/D-15 del usuario, no las toco.
- 2026-09-26  · UI-18 · en curso · DAT-19 (8f0d871) e INT-14 (5380624) tienen commit; agregadas también las filas pendientes UI-19 y UI-20 antes de iniciar la fase 2b.
- 2026-09-26  · UI-18 · bloqueada (falta API para descartar un pendiente) · DAT-19 expone crear, listar y confirmar, pero no descartar; archivos tocados: `plan/estado/Builder_UI.md`; no se corrieron pruebas porque no hubo implementación posible dentro de los archivos autorizados.
