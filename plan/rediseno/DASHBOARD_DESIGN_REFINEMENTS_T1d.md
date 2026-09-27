# Corrección T1d · Reorientación visual con referencias IDEAL

**Prioridad de autoridad visual para esta iteración:**
1. Funcionalidad existente → se conserva.
2. Las dos imágenes de `evidencia/IDEAL/` → autoridad visual.
3. Documentos anteriores (`DASHBOARD_DESIGN_SPEC.md`, `..._T1.md`, `..._T1b.md`, `..._T1c.md`) → sirven mientras no contradigan estas imágenes.
4. Implementación actual → no es referencia estética.

## Referencias visuales obligatorias

- `evidencia/IDEAL/Neumorphism_Dashboard_Professional.jpeg` — **referencia primaria**: simetría, uniformidad, geometría, ancho consistente de controles del mismo grupo, alturas consistentes, radios, ritmo vertical, alineación, relación icono + texto, composición general, sistema único, calidad profesional.
- `evidencia/IDEAL/Neumorphism_Dashboard_mobile_.jpeg` — **referencia complementaria**: tratamiento de superficies, profundidad, relación entre controles pequeños y grandes, calidad de las sombras, separación respecto al fondo, consistencia del relieve, modularidad.

## Comparación obligatoria

Comparar ambas referencias contra `evidencia/UI-21/componentes-390.png`. La implementación actual no representa todavía la estética objetivo. No tomarla como base estética ni pulirla incrementalmente: identificar qué decisiones visuales actuales impiden que se parezca al lenguaje de las referencias y corregirlas.

## Problema central

La implementación actual parece una colección de componentes a los que se les agregó `box-shadow`. Las referencias muestran un **sistema neumórfico integral**:

- todos los componentes pertenecen a la misma familia visual;
- la dirección de luz es consistente;
- las sombras tienen profundidad real;
- los radios mantienen una relación coherente;
- los controles se organizan geométricamente;
- el espacio entre elementos sigue un ritmo;
- la iconografía participa en la navegación;
- el texto confirma una acción, no construye toda la interfaz;
- el color es secundario;
- el volumen y la composición generan la jerarquía.

## Neumorfismo

Componentes interactivos principales claramente elevados, profundidad comparable a niveles 3–5 (`referencia-relieve-1-6.png`), nunca 1–2:

- highlight amplio y perceptible arriba/izquierda;
- sombra oscura amplia abajo/derecha;
- sombra de contacto suficiente;
- bordes suaves; transición gradual;
- superficie claramente separada del fondo;
- ningún aspecto de botón `outline`.

Visible a `390px` sin zoom.

## Prohibido como recurso principal

Bordes azules, verdes, rojos o ámbar; pills de colores; cards delineadas; botones outline; chips genéricos; contornos que compensen una sombra insuficiente.

Los colores de estado solo en iconos, pequeños acentos y señales puntuales. El cuerpo del componente pertenece al mismo sistema neumórfico neutro.

## Simetría

Los controles del mismo grupo comparten, cuando corresponda: altura, radio, eje de alineación, separación, profundidad, posición del icono y posición del texto. Ningún componente adopta una geometría arbitraria solo porque su texto tiene otra longitud. La referencia primaria guía esta decisión.

## Iconografía

Lucide no es el lenguaje visual obligatorio del futuro tablero principal. Los iconos deben tener mayor presencia y formar parte estructural de la navegación. No elegir una familia nueva definitiva si no hace falta para esta iteración. Lo importante: `icono reconocible + control neumórfico + texto de confirmación`.

## Interacción

Transición física coherente `elevado → presionado/hundido → elevado`: al tocar, reducir elevación, modificar sombras, sensación de presión, regreso suave al soltar. No resolverla solo con color.

## Componentes

- Reevaluar: C-01, C-02, Procesando, Éxito, Error, Deshabilitado, C-03, C-09. No asumir que conservan su aspecto actual.
- C-04, C-05 y C-06: más cerca de la dirección correcta; revisarlos contra las referencias para coherencia global.
- C-07: puede permanecer como enlace plano.
- C-10: desplazamiento horizontal resuelto; sin reinterpretación por ese motivo.

## Alcance funcional

No cambian datos, textos funcionales, acciones, reglas de negocio, flujos, backend ni comportamiento. Es una **reorientación visual**.

## Validación

La aceptación es visual, no porque compile, pasen pruebas, cumpla valores CSS, tenga sombras o respete tokens anteriores. Antes de terminar, generar evidencia a `390px` y comparar explícitamente profundidad, simetría, ritmo, alineación, consistencia de superficies, calidad de sombras y cohesión general contra las dos referencias.

El objetivo es que el Dashboard empiece a pertenecer claramente al **mismo lenguaje visual** que estas dos referencias.
