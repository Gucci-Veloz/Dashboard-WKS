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
| UI-07 | Conectar niveles 1 y 2 al servicio | pendiente | DAT-08 (D-3), UI-06 |
| UI-08 | Entrada al detalle bajo demanda | pendiente | UI-05 |
| UI-09 | Formulario editable y confirmación visible | pendiente | UI-03 |
| UI-10 | Detalle de oficinas | pendiente | DAT-09, UI-08, UI-09 |
| UI-11 | Detalle de inquilinos | pendiente | DAT-10, UI-10 |
| UI-12 | Detalle de contratos | pendiente | DAT-11, UI-11 |
| UI-13 | Detalle de pagos y registrar pago | pendiente | DAT-12, UI-12 |
| UI-14 | Rastro de Vania visible | pendiente | D-8, INT-02, INT-03, UI-07 |
| UI-15 | Botón seguir con Vania | pendiente | INT-08, UI-13 |
| UI-16 | Ajustar el detalle a los campos reales | pendiente | DAT-15, UI-13 |
| UI-17 | Efecto de sorpresa por calidad | pendiente | D-15, UI-07 |

## Qué sigue

UI-08 y UI-09 están libres. UI-07 sigue esperando DAT-08 (D-3), sin commit todavía.

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
- 2026-09-23 06:40 · UI-06 · hecha · ajusté las pruebas de UI-04 y UI-05, que asumían "ninguna lista" como ningún `ul`/`ol` en toda la página; con los indicadores (que sí son una lista y se muestran siempre) esa aserción era demasiado amplia. Las dejé apuntando a lo que de verdad importaba: que no aparezca la lista de asuntos. app/fuentes/cargar.py falló en la corrida completa, pero es de Builder_Datos y no lo toqué. Sigue UI-08 o UI-09; UI-07 sigue esperando DAT-08.
