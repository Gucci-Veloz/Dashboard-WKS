# Rediseño visual del Dashboard · Qué necesita Father

## Alcance

**Cambia solo el diseño:** cómo se ve el Dashboard y cómo responden los controles al tocarlos.
El estilo buscado es Apple-inspired Soft UI + Soft Structuralism + neumorfismo selectivo + microinteracciones + progressive disclosure.

**No cambia nada de la funcionalidad:** el acceso por link, las sesiones, los flujos, la confirmación, los pendientes, los duplicados y el reporte del día quedan como están. Cada pantalla conserva sus datos y sus acciones. Lo que cambia es cómo se presentan.

---

## 1. Diagnóstico de las 7 capturas actuales

Todas están tomadas en un teléfono de 390 px de ancho.

| # | Captura | Qué muestra |
|---|---|---|
| 1 | `evidencia/INT-14/entrada-390.png` | Pantalla de entrada (link vencido o sin sesión) |
| 2 | `evidencia/UI-03/componentes-390.png` | Muestrario de componentes base: tarjeta, botón y campo |
| 3 | `evidencia/UI-04/nivel1-tranquilo-390.png` | Pantalla principal con Works tranquilo |
| 4 | `evidencia/UI-04/nivel1-con_atencion-390.png` | Pantalla principal con cosas que necesitan atención |
| 5 | `evidencia/UI-05/nivel2-con_atencion-390.png` | Lista de asuntos que necesitan atención |
| 6 | `evidencia/UI-09/formulario-390.png` | Formulario de edición |
| 7 | `evidencia/UI-20/reporte-390.png` | Reporte del día |

Para cada captura necesito, con nombres técnicos:

- **Qué está mal:** jerarquía visual, profundidad y sombras, espaciado, tipografía, color, alineación, densidad de texto, bordes y radios.
- **Cómo debería quedar**, con la regla o el valor que lo corrige.

**Pantallas que existen pero no tienen captura:** la entrada a las cuatro áreas, las listas y fichas de oficinas, inquilinos, contratos y pagos, la ventana de confirmación, el aviso de duplicado y los cambios pendientes. Pueden quedar cubiertas por las reglas globales y los componentes. Solo describan alguna aparte si debe tener algo especial.

---

## 2. Estilo destino: el GIF traducido a reglas

El GIF no va a llegar al proyecto, así que necesito sus propiedades en valores, no en adjetivos. Por ejemplo, "sombra suave" no me sirve; "sombra de 8 px de desplazamiento, 20 px de difuminado y 12 % de opacidad" sí. Si no hay valor exacto, sirve un rango.

- **Color:** fondo, superficies, texto principal y secundario, acento, y colores de estado (bien, atención y error). Todo en hex.
- **Tipografía:** familia, tamaños, pesos e interlineado de cada nivel (frase principal, título, texto, dato, etiqueta).
- **Profundidad:** cuántos niveles hay y el valor de sombra de cada uno. Además, **qué elementos llevan neumorfismo y cuáles son planos** (eso es lo "selectivo").
- **Estructura (Soft Structuralism):** cómo se agrupan y separan los bloques: contenedores, separadores, retícula y alineación.
- **Forma:** radios de las esquinas por tipo de elemento.
- **Espacio:** la escala de espaciado y los márgenes de la pantalla.
- **Íconos:** si se usan, de qué juego, en qué estilo y con qué grosor.
- **Recursos externos:** si hace falta una fuente, un juego de íconos o una librería de fuera, su nombre exacto.

---

## 3. Controles y microinteracciones

Para cada tipo de control (botón principal, botón secundario, tarjeta que se puede tocar, campo de texto, interruptor o selector, pestaña, enlace, ventana emergente):

| Estado | Qué necesito |
|---|---|
| Reposo | Cómo se ve |
| Al pasar el mouse (escritorio) | Qué cambia |
| Al presionar | Qué cambia (se hunde, se encoge, cambia de color) y cuánto |
| Al soltar | Cómo regresa |
| Foco del teclado | Cómo se marca |
| Procesando | Qué ve la persona mientras espera |
| Éxito o error | Cómo lo comunica |
| Deshabilitado | Cómo se ve |

Para cada microinteracción: **duración en milisegundos, curva de movimiento y qué propiedad se anima** (sombra, escala, color, posición u opacidad).

---

## 4. Progressive disclosure

Por pantalla:

- **Qué se ve de entrada** y qué queda oculto hasta que se pide.
- **Con qué gesto se revela:** tocar, desplegar, deslizar o abrir una hoja desde abajo.
- **Cómo se anima** al abrir y al cerrar.

---

## 5. Teléfono y escritorio

El Dashboard se usa sobre todo en el teléfono. Para el escritorio basta con decir qué cambia: ancho máximo, columnas o controles que se reacomodan.

---

## 6. Cómo entregarlo

Un solo archivo Markdown con estas secciones:

1. **Reglas globales:** lo de la sección 2, con valores.
2. **Controles:** lo de la sección 3, cada uno con una clave (`C-01`, `C-02`…).
3. **Pantallas:** una por cada captura, más las especiales si las hay. Cada pantalla nombra los controles que usa, lo que se ve de entrada y lo que se revela después, y solo anota sus **excepciones** a las reglas globales.
4. **Criterios de aceptación:** de 2 a 4 frases comprobables por pantalla. Por ejemplo: "la frase de estado es el texto más grande", "al presionar un botón se hunde y cambia de color".

---

## 7. Qué decides tú y qué resuelvo yo

- **Tú:** todo lo que se ve y se siente, es decir, los valores, qué lleva profundidad, las microinteracciones y lo que se oculta o se muestra.
- **Yo:** cómo se programa, los valores intermedios que salgan de tu escala y la accesibilidad invisible (orden del foco, lectores de pantalla y la versión para quien desactiva las animaciones).
- Cada pantalla rediseñada llega con capturas para tu visto bueno. Si encuentro un hueco que cambia lo que se ve, te lo pregunto; no lo invento.

**No hace falta explicarme** el proyecto, Vania, la funcionalidad ni las reglas de operación. Eso ya lo conozco.
