# Dashboard Design Refinements · Tarea 1

## 0. Alcance

Este documento consolida los refinamientos visuales aprobados después de revisar la primera implementación de `DASHBOARD_DESIGN_SPEC.md`.

No sustituye la especificación principal.

Debe aplicarse como una capa de corrección sobre ella.

Estos ajustes afectan exclusivamente:

- contraste visual;
- calidad de sombras;
- profundidad;
- percepción de controles;
- tratamiento visual de enlaces;
- comportamiento visual de elementos deshabilitados;
- presentación del overlay;
- tratamiento responsive de tablas.

No modificar:

- funcionalidad;
- datos;
- textos funcionales;
- acciones;
- reglas de negocio;
- flujos;
- prioridades;
- backend.

---

# 1. C-01 · Botón principal

## Texto

Conservar:

`Registrar pago`

No abreviar ni reducir el tamaño del texto para igualarlo visualmente con otros botones.

## Ancho

C-01 puede ser naturalmente más ancho que C-02 debido a la longitud de su contenido y su mayor presencia visual.

No imponer el mismo ancho a ambos controles.

La diferencia debe ser moderada y resultar de:

- contenido;
- padding;
- proporción natural del componente.

No utilizar un ancho fijo excesivo.

## Sombra

La lógica neumórfica actual se conserva, pero la ejecución necesita refinamiento.

Especialmente en móvil a `390px`, mejorar:

- separación entre superficie y fondo;
- sombra oscura;
- highlight claro;
- blur;
- desplazamiento;
- balance entre ambos lados del control.

El highlight del lado superior/izquierdo no debe desaparecer contra el fondo ni generar una zona visualmente lavada.

---

# 2. C-02 · Botón secundario

## Texto

Conservar:

`Cancelar`

No sustituir por `Cancelar pago`, porque esa redacción implicaría una semántica funcional que no está establecida.

## Ancho

C-02 puede ser más compacto que C-01.

No aumentar artificialmente su ancho para igualarlo con `Registrar pago`.

Debe conservar:

- padding suficiente;
- presencia visual;
- proporción natural respecto al texto.

## Sombra

Aplicar el mismo refinamiento óptico definido para C-01.

C-02 debe seguir teniendo menor protagonismo que C-01 sin desaparecer visualmente.

---

# 3. Estado Procesando

El control en estado `Procesando` debe conservar la misma geometría base del botón al que sustituye.

La sombra actual necesita el mismo refinamiento de:

- contraste;
- highlight;
- blur;
- desplazamiento;
- separación respecto al fondo.

El cambio hacia `Procesando` no debe producir un salto visual de tamaño.

---

# 4. Estado Deshabilitado

El estado actual pierde demasiado su silueta, especialmente en móvil.

Debe continuar percibiéndose como secundario e inactivo, pero seguir siendo reconocible como control.

Añadir:

- contorno gris sutil;
- contraste suficiente entre superficie y fondo;
- sombra mínima o inexistente según el resultado óptico.

No depender únicamente de bajar la opacidad del texto.

El usuario debe poder reconocer la geometría completa del control sin necesidad de hacer zoom.

---

# 5. C-04 · Campo hundido

La dirección visual actual es correcta.

Debe aumentarse ligeramente la percepción de profundidad interior.

Refinar:

- `inset shadow`;
- contraste entre bordes internos;
- highlight interior;
- separación tonal respecto de la superficie general.

El objetivo es que el campo se perciba claramente **hundido**, manteniendo un resultado limpio y suave.

No exagerar el efecto hasta convertirlo en un hueco oscuro.

---

# 6. C-05 · Toggle

Mantener el toggle:

- compacto;
- reconocible;
- sin convertirlo en botón;
- sin aumentar artificialmente su tamaño.

La mejora debe concentrarse en la **pista hundida**.

Aumentar/refinar:

- sombra interior;
- profundidad perceptible;
- contraste entre pista y superficie;
- definición de la perilla.

La pista debe percibirse como una cavidad suave incluso a tamaño real en una pantalla móvil.

---

# 7. C-06 · Selector segmentado

La estructura conceptual actual se conserva.

Ejemplo:

`Hoy / Ayer`

El contenedor hundido y el segmento activo deben distinguirse con mayor claridad.

Refinar:

- profundidad de la base hundida;
- separación del segmento activo;
- sombra del elemento elevado;
- contraste entre estado activo e inactivo.

Aplicar la misma calibración óptica utilizada para C-01 y C-02 cuando corresponda.

---

# 8. C-07 · Enlace

C-07 permanece plano.

No añadir neumorfismo.

Mantener:

- color azul;
- ausencia de superficie elevada.

Añadir:

**subrayado visible.**

El subrayado debe permitir reconocer inmediatamente que se trata de un enlace y diferenciarlo de:

- texto informativo;
- etiquetas;
- botones.

Estados posteriores como hover, foco y presionado pueden modificar intensidad u opacidad, pero el enlace debe seguir siendo reconocible sin depender exclusivamente del color.

---

# 9. C-08 · Overlay

## Modal

La ventana modal conserva su profundidad `N3`.

Debe seguir siendo claramente una superficie elevada sobre el resto de la interfaz.

## Etiqueta `C-08 · Overlay`

Eliminar la cápsula gris pesada actual.

La etiqueta debe ser:

- plana;
- discreta;
- ligera;
- claramente secundaria.

No debe parecer:

- botón;
- chip interactivo;
- superficie elevada;
- mancha gris dentro del modal.

La profundidad pertenece al modal, no a su etiqueta descriptiva.

---

# 10. Contraste general entre fondo y superficies

El fondo casi blanco actual se conserva como dirección.

El problema está en que algunas superficies y controles se mezclan demasiado con él.

Aumentar la separación visual principalmente mediante:

1. mejor calibración de sombras;
2. diferencia tonal sutil entre superficie y fondo;
3. highlight mejor definido;
4. contorno muy discreto únicamente cuando sea necesario.

Evitar resolver el problema mediante:

- colores fuertes;
- bordes oscuros generalizados;
- sombras agresivas;
- aumento excesivo de saturación.

La interfaz debe continuar siendo:

- clara;
- suave;
- ligera;
- Soft UI.

Pero sus controles deben poder distinguirse inmediatamente a tamaño real.

---

# 11. Calidad óptica de las sombras

La arquitectura de profundidad definida originalmente sigue vigente.

El problema detectado no es el concepto de neumorfismo, sino la **calidad óptica de algunas sombras**.

Prioridad de calibración:

1. C-01;
2. C-02;
3. Procesando;
4. C-06;
5. C-05;
6. C-04.

Evaluar siempre las sombras primero en viewport móvil de `390px`.

Una sombra correcta debe:

- definir la forma sin crear bordes duros;
- conservar el highlight claro;
- mantener visible el lado izquierdo/superior;
- diferenciar la superficie del fondo;
- evitar apariencia borrosa o sucia;
- funcionar sin necesidad de zoom.

Después de conseguir una calibración satisfactoria en móvil, reutilizar la misma lógica proporcional en escritorio.

---

# 12. Tabla móvil

La solución queda aprobada.

No reducir:

- tipografía;
- contenido;
- número de columnas por motivos exclusivamente visuales.

La tabla debe vivir dentro de un contenedor con desplazamiento horizontal propio.

Conceptualmente:

```text
PÁGINA · 390px
│
└── CONTENEDOR DE TABLA
    │
    ├── ancho visible: viewport disponible
    ├── contenido interno: puede ser más ancho
    └── scroll horizontal propio
```

La página completa nunca debe producir desplazamiento horizontal.

No cortar columnas.

Puede utilizarse una señal visual discreta en el borde derecho para indicar que existe contenido adicional horizontal.

---

# 13. Móvil como referencia principal de calibración

Los problemas de sombra y contraste resultan especialmente evidentes en `390px`.

Por tanto:

- calibrar primero móvil;
- comprobar controles a tamaño real;
- evitar decisiones basadas únicamente en zoom;
- posteriormente validar escritorio.

El escritorio puede utilizar ajustes proporcionales cuando el mayor espacio modifique la percepción de profundidad.

---

# 14. Futuro tablero principal

Esta dirección queda confirmada conceptualmente, pero no forma parte de la implementación de esta tarea.

El Dashboard deberá contar posteriormente con una pantalla principal altamente visual e interactiva basada en:

- controles fácilmente reconocibles;
- iconos asociados a funciones;
- botones con sensación física;
- hundimiento al presionar;
- estados visuales;
- microinteracciones;
- menor dependencia del texto;
- experiencia dinámica e inmersiva.

Cada control representará una función real ya existente en el Dashboard.

La arquitectura concreta de ese tablero todavía no está definida.

---

# 15. Iconografía futura

**Lucide queda descartado como dirección iconográfica para el futuro tablero principal.**

No utilizar Lucide como referencia obligatoria para diseñar esos futuros controles visuales.

La familia o lenguaje iconográfico sustituto permanece pendiente de selección.

La elección deberá realizarse cuando se diseñe específicamente el tablero principal.

Este punto no bloquea los refinamientos de la Tarea 1.

---

# 16. Criterios de aceptación de esta tarea

La Tarea 1 puede considerarse consolidada cuando:

1. C-01, C-02, Procesando y C-06 presentan sombras claramente perceptibles y limpias a `390px`.
2. Los highlights claros no desaparecen contra el fondo.
3. C-01 y C-02 conservan anchos naturales diferentes sin que ninguno parezca desproporcionado.
4. C-04 se percibe claramente hundido.
5. La pista de C-05 se percibe claramente hundida sin aumentar el tamaño general del toggle.
6. C-07 se reconoce inmediatamente como enlace gracias a color + subrayado.
7. El estado Deshabilitado conserva una silueta visible aunque siga siendo visualmente secundario.
8. La etiqueta de C-08 deja de parecer una cápsula o botón.
9. El modal C-08 conserva su profundidad.
10. Los controles se distinguen del fondo sin abandonar la estética Soft UI.
11. La tabla móvil mantiene su contenido completo mediante scroll horizontal interno.
12. Ninguno de estos ajustes modifica funcionalidad, contenido ni reglas del Dashboard.

---

# Estado

**Tarea 1 de 3: especificación de refinamientos visuales consolidada.**

Los siguientes trabajos pueden continuar utilizando como base conjunta:

1. `DASHBOARD_DESIGN_SPEC.md`;
2. `DASHBOARD_DESIGN_REFINEMENTS_T1.md`.

En caso de contradicción visual entre ambos documentos respecto de los puntos tratados aquí, este documento representa la decisión más reciente.
