La dirección visual actual queda **APROBADA como base**.

No reconstruyas el sistema.
No cambies la geometría de los seis controles principales.
No cambies sus anchos, alturas, radios, separación, alineación, material ni nivel general de relieve.

Esta iteración es exclusivamente una **DELTA CORRECTION** sobre tres puntos pendientes.

Referencias visuales:

`/home/gusta/Projects/DASHBOARDS/Works/evidencia/IDEAL/Neumorphism_Dashboard_Professional.jpeg`

`/home/gusta/Projects/DASHBOARDS/Works/evidencia/IDEAL/Neumorphism_Dashboard_mobile_.jpeg`

---

# DELTA-01 · C-08 Overlay — corregir artefacto lateral

## Problema

C-08 presenta una franja gris vertical oscura en el extremo derecho del modal.

Visualmente parece:

- clipping;
- una capa parcialmente expuesta;
- una sombra contenida incorrectamente;
- o una pseudocapa sobresaliendo.

Ese artefacto NO pertenece al lenguaje visual aprobado.

## Acción

Inspecciona primero el DOM y los estilos computados de C-08.

Busca específicamente:

- `overflow`;
- `overflow: hidden`;
- pseudoelementos `::before` / `::after`;
- wrappers superpuestos;
- `box-shadow`;
- offsets;
- widths mayores al contenedor;
- transforms;
- backgrounds de capas padre/hijo.

Corrige la **causa raíz**.

No tapes la franja con otro elemento.
No añadas un parche del color del fondo.
No escondas arbitrariamente contenido.

## Resultado requerido

El modal debe mostrar una única silueta continua y simétrica.

```text
left edge  ≈ right edge
top radius ≈ top radius
```

No debe existir ninguna franja vertical independiente en ninguno de sus lados.

---

# DELTA-02 · Sistema iconográfico — unificación completa

## Problema

La geometría de los controles ya está bien, pero la iconografía todavía mezcla gramáticas visuales.

Actualmente conviven:

- iconos sólidos;
- iconos outline;
- círculos completos;
- círculos incompletos;
- check desnudo;
- símbolos contenidos;
- símbolos sin contenedor.

Esto rompe la cohesión visual.

## Objetivo

Todos los iconos pertenecientes a la misma familia de controles deben compartir:

```text
visual weight
stroke/fill strategy
bounding box
apparent size
alignment
optical density
```

### Restricciones

Para:

- C-01
- C-02
- Procesando
- Éxito
- Error
- Deshabilitado
- C-03

usa **una sola gramática iconográfica**.

No mezcles arbitrariamente:

```text
solid
outline
circled
uncircled
thin
heavy
```

## Dirección preferida

Usa como guía `Neumorphism_Dashboard_Professional.jpeg`.

Preferencia:

**glyphs sustanciales, simples y de peso óptico uniforme**, antes que iconos outline excesivamente delgados.

No significa que todos deban estar encerrados en círculos.

De hecho:

> NO añadas burbujas circulares alrededor de los iconos salvo que la propia semántica del símbolo las requiera.

Ejemplos:

- `Éxito` puede utilizar check.
- `Error` puede utilizar X.
- `Atención` puede utilizar `!`.
- `Procesando` utiliza spinner.

Pero todos deben percibirse pertenecientes al **mismo sistema gráfico**.

## Métrica

Para los iconos equivalentes:

```text
24px <= visual bounding box <= 28px
```

y:

```text
max(apparent_size) - min(apparent_size)
```

debe ser visualmente mínima.

Mantener los ejes X actuales, que ya quedaron correctos.

---

# DELTA-03 · C-04 — refinamiento de profundidad

C-04 NO necesita reconstrucción.

La dirección hundida es correcta.

El problema es únicamente que, ahora que los controles elevados mejoraron, C-04 tiene menor calidad óptica relativa.

## Acción

Refina únicamente su `inset shadow`.

Objetivo:

```text
IN1 actual → IN1+
```

Incrementar moderadamente:

- sombra interior inferior/derecha;
- highlight interior superior/izquierdo;
- percepción de cavidad.

No aumentar excesivamente:

- oscuridad;
- borde;
- contraste del fondo.

No convertirlo en:

```text
input convencional con borde
```

Debe seguir pareciendo una superficie excavada suavemente dentro del mismo material.

---

# ELEMENTOS BLOQUEADOS — NO TOCAR

No modificar salvo que sea indispensable para resolver uno de los tres DELTAs:

- geometría de C-01;
- geometría de C-02;
- Procesando;
- Éxito;
- Error;
- Deshabilitado;
- C-03;
- C-05;
- C-06;
- C-07;
- comportamiento horizontal de C-10;
- espaciado del grupo principal;
- ancho del panel;
- dirección global de iluminación;
- material general.

El sistema principal finalmente está funcionando.

No provoques regresiones mientras corriges detalles.

---

# ACCEPTANCE GATES

La iteración falla si ocurre cualquiera:

```text
FAIL-01
C-08 conserva cualquier franja lateral independiente.

FAIL-02
Los iconos siguen mezclando estilos incompatibles.

FAIL-03
Se introducen nuevamente burbujas arbitrarias alrededor de iconos.

FAIL-04
Se modifica la geometría aprobada del grupo principal sin necesidad técnica.

FAIL-05
C-04 termina pareciendo un input convencional con borde.

FAIL-06
Algún cambio provoca regresión en C-01, C-02, Procesando, Éxito, Error o Deshabilitado.
```

---

# VALIDACIÓN

Genera una nueva evidencia `390px`.

Comprueba visualmente únicamente:

1. C-08 limpio y simétrico.
2. Iconografía coherente como una sola familia.
3. C-04 ligeramente más profundo que antes.
4. Ninguna regresión en el sistema aprobado.

No generes otro documento de comparación.

No vuelvas a evaluar el diseño completo.

No rediseñes.

Corrige estos tres DELTAs, ejecuta las pruebas existentes y entrega la nueva captura.
