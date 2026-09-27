# Corrección T1c · Relieve neumórfico niveles 3–5

Capa sobre `DASHBOARD_DESIGN_SPEC.md`, `DASHBOARD_DESIGN_REFINEMENTS_T1.md` y `DASHBOARD_DESIGN_REFINEMENTS_T1b.md`. Si se contradicen, manda este documento.

**Referencia visual directa:** `plan/rediseno/referencia-relieve-1-6.png` (seis niveles de relieve; ábrela y mírala antes de empezar).

Rediseña ahora mismo los componentes indicados tomando como referencia visual directa la imagen de niveles de relieve neumórfico `1–6`.

## Objetivo visual

Los componentes neumórficos actuales tienen un relieve demasiado débil y varios de ellos ni siquiera se perciben como neumorfismo.

Los componentes interactivos principales deben percibirse aproximadamente en el rango visual **3–5** de la referencia, según su función. No superficies casi planas equivalentes a niveles 1–2.

El volumen debe ser claramente perceptible a tamaño real en móvil, sin necesidad de zoom.

## Componentes que deben rehacerse

- `C-01 · Registrar pago`
- `C-02 · Cancelar`
- `Procesando`
- `Éxito`
- `Error`
- `Deshabilitado`
- `C-03 · Tarjeta tocable`
- `C-09 · Atención`

## Regla neumórfica

El relieve se construye principalmente mediante: superficie clara; highlight visible arriba/izquierda; sombra oscura visible abajo/derecha; blur suficiente; separación óptica clara respecto al fondo; bordes suaves; volumen perceptible.

La forma debe parecer **elevada físicamente sobre la superficie**, no simplemente delimitada por un borde.

## Prohibido

No resolver estos componentes mediante: contorno completo azul, verde o rojo; apariencia de botón `outline`; apariencia de chip genérico; tarjeta con borde coloreado; label tipo framework; degradados que sustituyan el relieve; sombras tan débiles que desaparezcan contra el fondo.

## Éxito y Error

Mismo lenguaje neumórfico del resto. Sin borde completo verde o rojo como tratamiento principal. El estado se comunica con icono verde (`Éxito`) o rojo (`Error`), manteniendo superficie y relieve. El color de estado es un **acento**, no reemplaza el lenguaje visual del botón.

## C-03

Eliminar la dependencia del contorno azul. La condición interactiva se percibe por elevación, volumen, sombra y respuesta al tocar. No debe parecer una tarjeta `outline`.

## C-09 · Atención

Eliminar el tratamiento de badge/pill con contorno coloreado como recurso principal. Debe integrarse con el sistema Soft UI. La atención se comunica con icono o pequeño acento cromático, sin romper la superficie neumórfica.

## Deshabilitado

Sigue siendo reconocible como el mismo tipo de control. Menor contraste y menor profundidad, pero no desaparece ni parece una mancha plana.

## C-04, C-05 y C-06

No rehacer conceptualmente. Solo conservar o refinar su profundidad para mantener coherencia con la nueva calibración.

## C-07 y C-10

No modificar.

## C-01 y C-02

Mantener los textos `Registrar pago` y `Cancelar`. `Registrar pago` puede ser más ancho. No igualar anchos, no reducir la tipografía, no cambiar el texto de `Cancelar`.

## Prioridad

1. C-01 · 2. C-02 · 3. Procesando · 4. Éxito · 5. Error · 6. Deshabilitado · 7. C-03 · 8. C-09

## Criterio de aceptación (visual)

No se da por terminada porque las pruebas pasen. Antes de afirmar que quedó, verificar a `390px` que:

- C-01, C-02 y Procesando se ven claramente elevados;
- el relieve corresponde aproximadamente a los niveles 3–5 de la referencia;
- el lado superior/izquierdo conserva highlight visible;
- el lado inferior/derecho tiene sombra suficiente;
- Éxito y Error ya no parecen botones outline;
- C-03 ya no parece una tarjeta con borde azul;
- C-09 Atención ya no parece un badge genérico;
- los componentes siguen perteneciendo al mismo sistema visual.
