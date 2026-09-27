# Especificación visual e interactiva del Dashboard

## 0. Alcance y regla de interpretación

Este documento define exclusivamente el sistema visual e interactivo del Dashboard.

Dirección consolidada:

**Apple-inspired Soft UI + Soft Structuralism + neumorfismo selectivo + microinteracciones + progressive disclosure.**

No modifica:

- funcionalidad;
- reglas de negocio;
- datos;
- acciones disponibles;
- flujos;
- prioridades operativas;
- sesiones;
- confirmaciones;
- duplicados;
- pendientes;
- reportes.

Las capturas actuales se utilizan únicamente como **anti-referencia visual**.

Los textos y datos visibles en ellas no determinan:

- qué información es importante;
- qué debe existir;
- qué debe ocultarse;
- qué debe mostrarse primero;
- qué acción tiene prioridad.

La regla del rediseño es:

> La profundidad, la forma, el estado, la posición, la iconografía y la interacción deben comunicar tanto como sea razonable antes de depender del texto.

---

# 1. Reglas globales

## 1.1 Dirección visual

La interfaz debe sentirse:

- limpia;
- suave;
- precisa;
- estructurada;
- táctil;
- ligera;
- claramente interactiva cuando corresponda.

No se busca neumorfismo global.

El neumorfismo se utiliza únicamente cuando la profundidad comunica:

- interacción;
- presión;
- selección;
- estado;
- activación.

Los elementos puramente informativos permanecen principalmente planos.

---

## 1.2 Color

| Token | Valor |
|---|---|
| Fondo general | `#EEF1F5` |
| Superficie base | `#F3F6F9` |
| Superficie elevada | `#F8FAFC` |
| Superficie hundida | `#E7ECF2` |
| Separadores | `#D7DEE7` |
| Texto principal | `#202734` |
| Texto secundario | `#596575` |
| Texto tenue | `#7B8794` |
| Acento principal | `#0A66D9` |
| Bien | `#2D7A57` |
| Bien suave | `#E6F4EC` |
| Atención | `#9A5A00` |
| Atención suave | `#FFF3DC` |
| Error | `#B83232` |
| Error suave | `#FDECEC` |

El color de estado debe utilizarse principalmente en:

- iconos;
- indicadores;
- bordes;
- pequeños fondos tonales;
- estados activos.

No llenar grandes superficies con colores intensos salvo que la propia funcionalidad lo requiera.

---

# 1.3 Tipografía

Familia principal:

**Inter Variable**

Fallback:

`-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

| Nivel | Tamaño móvil | Peso | Interlineado |
|---|---:|---:|---:|
| Frase principal / estado | `36px` | `700` | `40px` |
| Título principal | `28px` | `700` | `34px` |
| Título secundario | `22px` | `650` | `28px` |
| Dato destacado | `20px` | `650` | `26px` |
| Texto normal | `16px` | `450` | `24px` |
| Etiqueta | `13px` | `600` | `18px` |
| Texto auxiliar | `13px` | `450` | `19px` |
| Caption | `12px` | `500` | `16px` |

En escritorio:

- frase principal: hasta `44px / 50px`;
- título principal: hasta `32px / 38px`.

Una frase principal no debe utilizar tamaño display si produce más de aproximadamente dos líneas.

El tamaño no debe ser el único recurso para crear jerarquía.

---

# 1.4 Profundidad

El sistema utiliza cinco niveles funcionales.

## N0 — Plano

```css
box-shadow: none;
```

Usar en:

- texto;
- etiquetas;
- superficies informativas;
- tablas;
- separadores;
- contenedores estructurales;
- tarjetas estáticas.

---

## N1 — Elevación suave

```css
box-shadow:
  4px 4px 10px rgba(42, 52, 65, 0.10),
  -4px -4px 10px rgba(255, 255, 255, 0.72);
```

Usar en:

- controles secundarios;
- pequeños botones interactivos;
- tarjetas tocables de baja prominencia.

---

## N2 — Elevación interactiva

```css
box-shadow:
  8px 8px 18px rgba(42, 52, 65, 0.13),
  -8px -8px 18px rgba(255, 255, 255, 0.82);
```

Usar en:

- botón principal;
- controles importantes;
- selector activo;
- tarjeta interactiva destacada.

---

## N-1 — Hundido

```css
box-shadow:
  inset 3px 3px 7px rgba(42, 52, 65, 0.12),
  inset -3px -3px 7px rgba(255, 255, 255, 0.76);
```

Usar en:

- campos;
- pistas de interruptores;
- controles seleccionables contenidos;
- estado presionado cuando corresponda.

---

## N3 — Overlay

```css
box-shadow:
  0 18px 48px rgba(32, 39, 52, 0.18),
  0 2px 8px rgba(32, 39, 52, 0.08);
```

Usar exclusivamente en:

- modal;
- hoja inferior;
- menú flotante.

Los overlays no utilizan neumorfismo dual. Utilizan elevación convencional.

---

# 1.5 Qué lleva neumorfismo

## Sí

- botones;
- botones de icono;
- toggles;
- selectores;
- segmentos activos;
- campos hundidos;
- tarjetas realmente tocables;
- determinados indicadores interactivos.

## No

- fondo general;
- bloques de texto;
- títulos;
- etiquetas;
- tarjetas puramente informativas;
- tablas;
- agrupadores estructurales;
- cada sección de una pantalla;
- cada fila simplemente por existir.

Una superficie elevada debe implicar interacción o jerarquía real.

---

# 1.6 Soft Structuralism

La estructura debe percibirse principalmente mediante:

- alineación;
- espacio;
- agrupación;
- escala;
- separadores;
- cambios sutiles de superficie.

No mediante una tarjeta independiente alrededor de cada fragmento.

## Retícula

Unidad base:

`4px`

Escala principal:

`4 / 8 / 12 / 16 / 24 / 32 / 40 / 48 / 64px`

## Márgenes

Móvil:

`20px`

Pantallas muy estrechas:

mínimo `16px`

Escritorio:

`32–48px`

## Separación vertical

- elementos relacionados: `8–12px`;
- controles dentro de grupo: `12–16px`;
- bloques: `24px`;
- secciones: `32–40px`;
- secciones principales: `48px`.

---

# 1.7 Forma

| Elemento | Radio |
|---|---:|
| Elemento pequeño | `10px` |
| Campo | `14px` |
| Botón | `16px` |
| Tarjeta interactiva | `20px` |
| Contenedor destacado | `22px` |
| Modal | `24px` |
| Hoja inferior | `28px 28px 0 0` |
| Chip / pill | `999px` |

No usar el mismo radio indiscriminadamente.

---

# 1.8 Iconografía

Juego:

**Lucide Icons**

Estilo:

- outline;
- extremos redondeados;
- sin relleno como norma;
- grosor uniforme.

Valores:

- tamaño estándar: `20px`;
- icono pequeño: `16px`;
- icono destacado: `24px`;
- estado principal: `28–32px`;
- grosor: `1.75px`.

Los iconos deben comunicar:

- estado;
- acción;
- categoría;
- dirección;
- confirmación.

No utilizarlos como decoración arbitraria.

No usar emoji como iconografía funcional.

---

# 1.9 Recursos externos

- **Inter Variable**
- **Lucide Icons**

No se requiere framework visual adicional.

El frontend puede continuar con HTML + CSS + `app.js`.

---

# 1.10 Densidad y dependencia del texto

Evitar como patrón predeterminado:

`tarjeta → título → párrafo → otra tarjeta → otro párrafo`

Antes de añadir texto explicativo, evaluar si puede comunicarse mediante:

- estado;
- icono;
- posición;
- indicador;
- número;
- control;
- cambio de superficie.

Los párrafos explicativos deben tener un ancho máximo aproximado de `56ch`.

---

# 1.11 Progressive disclosure

No se deduce la importancia de ningún dato a partir de las capturas actuales.

Regla global:

**ningún dato ni acción existente se oculta automáticamente por el rediseño.**

Solo puede pasar a segundo nivel información que ya esté identificada por la aplicación como:

- auxiliar;
- detalle;
- explicación;
- metadata secundaria;
- ayuda.

Si esa clasificación no existe, el contenido permanece visible.

Patrones permitidos para revelar información secundaria:

- expansión dentro del bloque;
- sección desplegable;
- hoja inferior en móvil;
- modal cuando la acción ya requiera contexto aislado.

No utilizar swipe como único método para descubrir información.

---

# 1.12 Movimiento

## Motion tokens

| Token | Duración | Curva |
|---|---:|---|
| Instant | `90ms` | `cubic-bezier(.2,0,0,1)` |
| Fast | `120ms` | `cubic-bezier(.2,0,0,1)` |
| Standard | `180ms` | `cubic-bezier(.2,.8,.2,1)` |
| Emphasis | `240ms` | `cubic-bezier(.22,1,.36,1)` |
| Overlay | `280ms` | `cubic-bezier(.22,1,.36,1)` |

Propiedades preferidas:

- `transform`;
- `opacity`;
- `box-shadow`;
- `background-color`;
- `border-color`.

Evitar animar dimensiones grandes cuando pueda utilizarse transformación.

No utilizar movimiento continuo sin función.

---

# 2. Controles

# C-01 · Botón principal

## Reposo

- superficie `#F3F6F9`;
- nivel `N2`;
- radio `16px`;
- altura mínima `48px`;
- texto principal;
- icono opcional de `20px`.

## Hover

`120ms`

- `translateY(-1px)`;
- sombra aumenta aproximadamente un 10 %.

## Presionado

`90ms`

```text
translateY(1px)
scale(0.985)
```

Profundidad cambia temporalmente de `N2` a `N-1`.

## Soltar

`180ms`

Regresa a reposo con curva Standard.

## Foco

Anillo exterior:

`3px rgba(10,102,217,0.24)`

más borde `#0A66D9`.

## Procesando

- ancho no cambia;
- contenido permanece centrado;
- spinner de `16–18px`;
- profundidad `N1`;
- sin nueva interacción.

## Éxito

- icono de confirmación;
- señal `#2D7A57`;
- transición `180ms`.

## Error

- icono correspondiente;
- señal `#B83232`;
- transición `180ms`.

## Deshabilitado

- nivel `N0`;
- opacidad visual aproximada `0.45`;
- sin respuesta de profundidad.

---

# C-02 · Botón secundario

Igual a C-01 salvo:

- nivel inicial `N1`;
- menor protagonismo;
- acento reservado al icono, estado o foco;
- presión cambia a `N-1`.

---

# C-03 · Tarjeta tocable

Solo utilizar si la superficie realmente ejecuta una acción.

## Reposo

- superficie `#F3F6F9`;
- nivel `N1`;
- radio `20px`;
- padding `16–20px`.

## Hover

- `translateY(-1px)`;
- transición `120ms`;
- profundidad hacia `N2`.

## Presionado

- `scale(0.99)`;
- `translateY(1px)`;
- sombra reducida;
- `90ms`.

## Activo o seleccionado

- borde `1px solid rgba(10,102,217,.32)`;
- indicador visual de acento.

Una tarjeta estática no utiliza C-03.

---

# C-04 · Campo de texto

## Reposo

- superficie `#E7ECF2`;
- profundidad `N-1`;
- radio `14px`;
- altura mínima `48px`;
- padding horizontal `14px`.

## Hover

Borde:

`#C7D0DB`

Duración:

`120ms`

## Foco

- borde `#0A66D9`;
- anillo exterior `3px rgba(10,102,217,.18)`;
- sombra hundida ligeramente reducida;
- `180ms`.

## Éxito

- borde `#2D7A57`;
- icono pequeño opcional.

## Error

- borde `#B83232`;
- fondo tonal máximo `#FDECEC`;
- mensaje asociado si la aplicación ya lo proporciona.

## Deshabilitado

- fondo `#E4E9EF`;
- texto tenue;
- sombra reducida.

---

# C-05 · Interruptor / selector

## Estructura

Pista:

- profundidad `N-1`;
- radio pill.

Perilla:

- profundidad `N2`;
- forma circular.

## Activación

Movimiento:

`180ms cubic-bezier(.2,.8,.2,1)`

Propiedades:

- `transform`;
- `background-color`;
- `box-shadow`.

El estado debe ser reconocible mediante posición y apariencia sin depender exclusivamente de `ON/OFF`.

## Presionado

Perilla:

`scale(0.94)`

durante `90ms`.

---

# C-06 · Pestaña / control segmentado

Contenedor:

- superficie hundida `N-1`;
- padding `4px`;
- radio `14–16px`.

Segmento activo:

- superficie elevada;
- nivel `N1`;
- transición `180ms`.

Segmentos inactivos:

- planos;
- sin sombra individual.

---

# C-07 · Enlace

No neumórfico.

## Reposo

- color `#0A66D9`;
- peso `500`.

## Hover

- opacidad `0.82`;
- subrayado discreto.

## Presionado

- opacidad `0.65`;
- `90ms`.

## Foco

Anillo o subrayado visible de acento.

Un enlace no debe competir visualmente con un botón principal.

---

# C-08 · Modal / hoja inferior

## Escritorio

Modal centrado:

- nivel `N3`;
- radio `24px`;
- ancho máximo según contenido.

## Móvil

Hoja inferior:

- borde superior `28px`;
- nivel `N3`.

## Backdrop

```text
rgba(25,32,42,.24)
blur: 10px
```

## Apertura

`280ms`

- opacidad `0 → 1`;
- `translateY(16px) → 0`.

## Cierre

`240ms`

Proceso inverso.

---

# C-09 · Indicador de estado

Elemento principalmente informativo.

No utilizar sombra neumórfica por defecto.

Puede combinar:

- icono;
- color tonal;
- pequeño punto;
- etiqueta corta.

Debe comunicar estado sin depender exclusivamente del color.

Radio:

`999px` si es chip.

Padding:

`6px 10px`.

---

# C-10 · Tabla / conjunto de registros

La tabla es una excepción deliberada a la baja densidad.

## Escritorio

- superficie plana;
- `N0`;
- encabezado diferenciado por peso y tono;
- separadores de `1px`;
- padding vertical mínimo `12px`;
- sin tarjeta individual por fila.

## Móvil

No debe producir overflow horizontal de la página.

Si la aplicación no define qué columnas son secundarias:

- conservar todas;
- utilizar contenedor interno con `overflow-x: auto`;
- indicar visualmente que existe contenido horizontal;
- no cortar columnas.

No decidir qué columnas ocultar basándose en los datos de prueba.

Si en el futuro la aplicación clasifica columnas primarias/secundarias, podrá utilizarse progressive disclosure.

---

# 3. Reglas de teléfono y escritorio

## Teléfono

Diseño principal.

Hasta `767px`:

- una columna;
- margen lateral `20px`;
- controles principales de ancho completo cuando beneficie su uso;
- separación vertical como estructura dominante;
- ningún overflow horizontal del documento;
- overlays importantes como hoja inferior.

## Tablet

`768–1023px`

- contenido máximo aproximado `840px`;
- una o dos columnas únicamente cuando los grupos sean independientes.

## Escritorio

Desde `1024px`:

- ancho máximo general `1120px`;
- centrado;
- márgenes `32–48px`;
- pueden aparecer dos columnas cuando no alteren el orden lógico;
- formularios: máximo aproximado `680px`;
- listas: `760–840px` cuando no necesiten ancho completo;
- reportes/tablas: pueden utilizar hasta `1120px`.

No ampliar indefinidamente los bloques de texto.

---

# 4. Anti-patrones globales detectados en las capturas actuales

Las capturas actuales se utilizan únicamente para detectar problemas visuales.

Se observan de forma recurrente:

- dependencia excesiva del texto para comunicar estado;
- tarjetas utilizadas como contenedor predeterminado;
- sombras que no distinguen función;
- componentes estáticos e interactivos con profundidad parecida;
- grandes áreas vacías sin función estructural;
- jerarquía basada excesivamente en tamaño tipográfico;
- etiquetas tipo chip utilizadas como sustituto de visualización;
- campos con apariencia cercana al control nativo del navegador;
- botones cuya profundidad no representa claramente sus estados;
- ritmo vertical irregular;
- tratamiento poco diferenciado entre información y acción;
- escasa iconografía funcional;
- poca retroalimentación visual de estados;
- tablas no adaptadas al ancho móvil;
- enlaces visualmente desconectados del resto del sistema;
- falta de una escala consistente de radios;
- ausencia de una gramática clara entre superficie plana, elevada y hundida.

El rediseño debe eliminar estos patrones sin utilizar el contenido visible como criterio funcional.

---

# 5. Pantallas

Las siguientes reglas describen únicamente diferencias visuales respecto del sistema global.

---

## S-01 · `entrada-390.png`

### Problemas visuales a corregir

En la captura asociada se observa:

- exceso de protagonismo del texto grande;
- repetición de superficies elevadas;
- jerarquía dependiente de bloques textuales;
- controles y enlaces con lenguajes visuales diferentes;
- ritmo vertical poco estructurado.

### Destino

La pantalla de entrada debe utilizar una composición simple y concentrada.

Ancho máximo del bloque principal:

`480px`

La superficie general permanece plana.

Si existe una única acción principal, utilizar C-01.

Los mensajes de estado utilizan:

- icono de estado;
- título;
- texto auxiliar solo cuando exista;
- acción existente.

No envolver todo dentro de una gran tarjeta neumórfica.

### Progressive disclosure

No ocultar contenido funcional.

Información auxiliar ya clasificada como secundaria puede revelarse dentro del mismo bloque.

### Controles

- C-01;
- C-07;
- C-09 cuando exista un estado.

### Criterios de aceptación

1. El estado principal puede identificarse sin recorrer varias superficies elevadas.
2. La pantalla no utiliza más de un nivel de profundidad principal simultáneamente.
3. Los enlaces y acciones pertenecen claramente al mismo sistema visual.
4. Ningún dato o acción se elimina por motivos estéticos.

---

## S-02 · `componentes-390.png`

### Problemas visuales a corregir

La captura muestra:

- profundidad aplicada sin una jerarquía funcional suficientemente clara;
- superficies estáticas e interactivas visualmente similares;
- radios demasiado homogéneos;
- sombras grandes para elementos con poca importancia;
- campo, botón, tarjeta y enlace sin un sistema único de estados.

### Destino

Esta pantalla debe demostrar explícitamente la gramática:

```text
plano → elevado → presionado/hundido → overlay
```

Los componentes estáticos usan N0.

Los controles interactivos utilizan N1/N2 y N-1 según estado.

Los campos utilizan N-1.

Los enlaces permanecen planos.

### Progressive disclosure

No aplica como requisito de demostración.

### Controles

Debe permitir comprobar visualmente:

- C-01;
- C-02;
- C-03;
- C-04;
- C-05;
- C-06;
- C-07;
- C-09.

### Criterios de aceptación

1. Un observador puede distinguir qué elementos son interactivos sin leer una explicación.
2. Los componentes estáticos no parecen botones.
3. El estado presionado produce un cambio perceptible de profundidad.
4. Todos los componentes respetan la misma escala de radios, espacio y movimiento.

---

## S-03 · `nivel1-tranquilo-390.png`

### Problemas visuales a corregir

Se observa:

- encabezado sobredimensionado respecto al resto de la pantalla;
- gran cantidad de espacio vacío sin estructura;
- información resumida expresada casi únicamente mediante texto;
- chips textuales como principal recurso de estado;
- poca riqueza visual para comunicar normalidad.

### Destino

La pantalla debe comunicar su estado mediante una combinación de:

- jerarquía;
- indicador C-09;
- iconografía;
- espacio;
- superficie.

La normalidad debe sentirse visualmente estable y ligera.

No llenar la pantalla con tarjetas para compensar el espacio disponible.

Los bloques informativos estáticos deben permanecer planos.

### Progressive disclosure

No ocultar datos existentes por inferencia.

Los detalles explícitamente secundarios pueden quedar tras el mecanismo existente de acceso a detalle.

### Controles

- C-03 únicamente donde ya exista interacción;
- C-07;
- C-09.

### Criterios de aceptación

1. El estado general se reconoce antes de leer todos los textos.
2. Los elementos estáticos no utilizan profundidad que sugiera interacción.
3. El espacio vacío se percibe intencional y estructurado.
4. La pantalla no depende de una colección de chips textuales para comunicar su estado.

---

## S-04 · `nivel1-con_atencion-390.png`

### Problemas visuales a corregir

Se observa:

- texto dominante;
- sucesión de tarjetas de igual peso;
- explicaciones largas visibles simultáneamente;
- escasa diferenciación visual entre estado, resumen y detalle;
- profundidad repetida sin función clara;
- chips textuales como resumen secundario.

### Destino

El estado de atención debe utilizar:

- color tonal de atención `#FFF3DC`;
- indicador `#9A5A00`;
- iconografía C-09;
- jerarquía espacial.

No convertir cada información en una gran tarjeta elevada.

Una superficie solo utiliza C-03 si realmente es tocable.

La atención debe distinguirse visualmente sin llenar grandes superficies de color.

### Progressive disclosure

No se decide qué contenido ocultar mediante los ejemplos de la captura.

Los bloques ya clasificados como detalle pueden utilizar expansión o el mecanismo existente de navegación.

### Controles

- C-03 cuando corresponda;
- C-07;
- C-09.

### Criterios de aceptación

1. El estado de atención es reconocible por forma, señal e iconografía, no únicamente por texto.
2. Las superficies estáticas no simulan botones.
3. Los diferentes bloques no poseen automáticamente la misma elevación.
4. El diseño conserva exactamente las acciones y datos definidos por la aplicación.

---

## S-05 · `nivel2-con_atencion-390.png`

### Problemas visuales a corregir

Se observa:

- repetición de tarjetas voluminosas;
- alta dependencia de párrafos;
- jerarquía similar entre elementos consecutivos;
- grandes sombras alrededor de contenido informativo;
- escasa diferenciación entre resumen y detalle;
- ritmo vertical pesado.

### Destino

Las colecciones deben sentirse como una lista estructurada, no como una pila de tarjetas independientes.

Reglas:

- separación entre elementos: `12px`;
- superficies estáticas: N0;
- separador o cambio tonal cuando baste para agrupar;
- C-03 solo si todo el elemento es tocable;
- indicador de estado compacto mediante C-09.

### Progressive disclosure

Si un elemento ya dispone de detalle secundario reconocido por la aplicación:

- móvil: expansión dentro del elemento o navegación existente;
- escritorio: mismo comportamiento, sin inventar paneles nuevos.

Si no existe clasificación primaria/secundaria, conservar el contenido visible.

### Controles

- C-03 cuando sea interactivo;
- C-07;
- C-09.

### Criterios de aceptación

1. La lista puede recorrerse visualmente sin percibir cada elemento como una tarjeta independiente de gran peso.
2. El espacio entre elementos sustituye parte de las sombras actuales.
3. Un elemento tocable y uno estático tienen tratamientos diferentes.
4. Ningún texto de prueba determina qué información se oculta.

---

## S-06 · `formulario-390.png`

### Problemas visuales a corregir

Se observa:

- campos cercanos al aspecto nativo del navegador;
- falta de relación visual entre campos y sistema de superficies;
- botón con profundidad desconectada de los campos;
- gran espacio residual;
- poca estructura de agrupación;
- estados de foco, validación o procesamiento no visibles en la captura.

### Destino

Ancho máximo:

`680px`

En móvil:

`100%`

Campos:

C-04.

Separación:

- etiqueta → campo: `8px`;
- campo → siguiente grupo: `16px`;
- último campo → acción: `24px`.

El botón principal utiliza C-01.

No introducir tarjetas alrededor del formulario salvo agrupación funcional real.

### Progressive disclosure

Los campos existentes permanecen visibles.

Texto de ayuda opcional puede aparecer:

- al foco;
- tras una acción explícita;
- cuando la propia aplicación ya lo considere auxiliar.

### Controles

- C-01;
- C-04;
- otros controles únicamente si ya existen funcionalmente.

### Criterios de aceptación

1. Todos los campos comparten un estado hundido coherente.
2. El foco es perceptible mediante borde, anillo y cambio sutil de profundidad.
3. El botón responde físicamente al presionarse.
4. El formulario no utiliza contenedores decorativos para llenar espacio vacío.

---

## S-07 · `reporte-390.png`

### Problemas visuales a corregir

Se observa:

- tabla más ancha que el viewport;
- contenido cortado;
- alta densidad sin mecanismo visual de escaneo;
- encabezados y celdas con separación limitada;
- control de fecha visualmente nativo e inconsistente;
- inexistencia de una superficie clara que contenga el overflow;
- enlace inferior desconectado del sistema.

### Destino

El reporte constituye una excepción válida de alta densidad.

Utilizar C-10.

La tabla permanece plana.

No añadir sombras por fila.

Encabezado:

- peso `600`;
- tamaño `13px`;
- superficie sutil `#E7ECF2`.

Celdas:

- `14px / 20px`;
- padding mínimo `12px`.

Separadores:

`1px solid #D7DEE7`

Control de fecha:

C-04 adaptado al tipo correspondiente.

### Móvil

El documento nunca debe exceder `390px`.

La tabla se contiene dentro de su propia región desplazable horizontalmente cuando sea necesario.

No cortar datos.

No ocultar columnas basándose en ejemplos de contenido.

### Escritorio

La tabla puede utilizar hasta `1120px`.

Si cabe completamente, desaparece la necesidad de desplazamiento horizontal.

### Progressive disclosure

Por defecto no ocultar columnas.

Solo podrá colapsarse información cuando exista una clasificación formal de columnas primarias/secundarias independiente de las capturas.

### Controles

- C-04;
- C-07;
- C-10.

### Criterios de aceptación

1. A `390px` no existe overflow horizontal del documento.
2. Ninguna columna queda cortada fuera de un contenedor controlado.
3. La tabla no utiliza tarjetas ni sombras por fila.
4. El control de fecha pertenece visualmente al mismo sistema que los demás campos.

---

# 6. Pantallas sin captura específica

## Entrada a áreas, listas y fichas

Aplicar:

- reglas globales;
- C-03 solo a elementos realmente tocables;
- C-09 para estados;
- estructura mediante espacio antes que tarjetas.

No requieren un lenguaje visual independiente.

## Ventana de confirmación

Utilizar C-08.

No añadir nuevas acciones.

El botón principal y secundario deben conservar las acciones ya definidas.

## Aviso de duplicado

Utilizar C-08 + C-09.

El estado puede utilizar tono de atención o error según la clasificación que ya tenga la aplicación.

No inferir esa clasificación desde el diseño.

## Cambios pendientes

Aplicar C-09 para estado.

Si existe interacción asociada, utilizar el control correspondiente.

La mera presencia de información pendiente no convierte automáticamente el contenedor en una tarjeta elevada.

---

# 7. Reglas de aceptación global

El rediseño se considera coherente únicamente si cumple simultáneamente estas condiciones:

1. La profundidad comunica función y no decoración.
2. Los componentes estáticos e interactivos pueden distinguirse visualmente.
3. Los controles presentan feedback visible al presionarse.
4. Los campos se perciben hundidos y los botones interactivos elevados.
5. La interfaz depende menos del texto para comunicar estados.
6. La iconografía tiene función semántica y no ornamental.
7. No todo el contenido está encerrado en tarjetas.
8. El espacio y la alineación participan activamente en la estructura.
9. A `390px` ninguna pantalla produce overflow horizontal del documento.
10. Las tablas contienen su propio overflow cuando sea necesario.
11. Los colores de estado se utilizan como señales, no como decoración masiva.
12. Las microinteracciones utilizan las duraciones y curvas del sistema.
13. Ninguna captura actual determina reglas de negocio, prioridad o arquitectura de información.
14. Ningún dato o acción existente desaparece por una decisión puramente estética.
15. Progressive disclosure solo actúa sobre información ya reconocida como secundaria.
16. La interfaz puede evolucionar sin depender de React, Tailwind u otro framework frontend.
17. Todos los componentes deben poder explicarse mediante el mismo vocabulario:

**plano → elevado → hundido → activo → overlay**

---

# 8. Síntesis técnica

El Dashboard adopta un sistema **Apple-inspired Soft UI** estructurado mediante **Soft Structuralism**, con **neumorfismo selectivo** reservado para componentes cuyo relieve comunica interacción o estado.

El fondo y la estructura permanecen mayormente planos. Los controles interactivos pueden elevarse; los campos y pistas pueden hundirse; la presión modifica físicamente la profundidad; los overlays utilizan elevación convencional.

La interfaz reduce dependencia textual mediante iconografía funcional, indicadores de estado, jerarquía espacial, superficies y comportamiento interactivo.

Las microinteracciones utilizan transformaciones breves de entre `90ms` y `280ms`, con movimiento funcional y feedback inmediato.

El progressive disclosure forma parte del sistema, pero no se utiliza para inferir importancia a partir de contenido de prueba: ningún dato ni acción existente se oculta salvo que la propia aplicación lo clasifique como secundario.

El diseño está optimizado primero para `390px` y escala posteriormente a escritorio, manteniendo HTML + CSS + `app.js` sobre la arquitectura existente.
