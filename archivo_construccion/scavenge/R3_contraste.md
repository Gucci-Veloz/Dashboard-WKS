# R3 · Neumorphism y contraste en móvil

## Fuentes consultadas
- W3C WCAG 2.2 — Understanding SC 1.4.11 Non-text Contrast: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- W3C WCAG 2.2 — Understanding SC 1.4.3 Contrast (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C WCAG 2.2 — Understanding SC 1.4.6 Contrast (Enhanced): https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html
- W3C WCAG 2.2 — Understanding SC 2.4.11 Focus Not Obscured (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- W3C WCAG 2.2 — Understanding SC 2.4.13 Focus Appearance: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html
- Medium (Xurxe Toivo García) — "For a more accessible Neumorphism (Soft UI)": https://medium.com/@xurxe/accessible-neumorphism-soft-ui-992286900bfa
- UX Collective (Michael J. Fordham) — "Neumorphism: can we make it more accessible?": https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28
- Built In — "What Neumorphism Style Says About the State of UI Design": https://builtin.com/articles/neumorphism-accessibility
- CodeFronts — "Accessible Neumorphism That Passes Contrast": https://codefronts.com/design-styles/css-neumorphism/accessible-neumorphism-that-passes-contrast/
- WebAIM — Contrast Checker: https://webaim.org/resources/contrastchecker/

## Hechos

**Contraste de texto (WCAG 2.2)**
- H1: SC 1.4.3 (Contrast Minimum, nivel AA) exige contraste mínimo de **4.5:1** para texto normal, y **3:1** para texto grande (definido como 18pt / ~24px, o 14pt/~18.67px en negrita). Texto decorativo, inactivo, de logotipo o no visible queda exento. Fuente: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- H2: SC 1.4.6 (Contrast Enhanced, nivel AAA) exige **7:1** para texto normal y **4.5:1** para texto grande. Es un nivel más estricto que AA, pensado para compensar pérdida de sensibilidad al contraste equivalente a visión 20/80. Fuente: https://www.w3.org/WAI/WCAG22/Understanding/contrast-enhanced.html

**Contraste no textual — el criterio más relevante para neumorphism**
- H3: SC 1.4.11 (Non-text Contrast, nivel AA) exige contraste de al menos **3:1 contra el color adyacente** para: (a) la información visual necesaria para identificar componentes de interfaz y sus estados (bordes de botones/inputs, indicador de foco, estado marcado de un checkbox, posición de un toggle), y (b) objetos gráficos necesarios para entender el contenido. No se exige que todo el componente cumpla el ratio, solo las partes que identifican su límite o estado. Componentes inactivos quedan exentos. Cita textual: "The visual presentation of the following have a contrast ratio of at least 3:1 against adjacent color(s): User Interface Components... Graphical Objects...". Fuente: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

**Foco de teclado**
- H4: SC 2.4.11 (Focus Not Obscured Minimum, nivel AA, nuevo en WCAG 2.2) exige que el indicador de foco de teclado no quede completamente oculto por contenido creado por el autor (headers pegajosos, banners, chats). Ocultamiento parcial se tolera en AA; ocultamiento total es una falla. Fuente: https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
- H5: SC 2.4.13 (Focus Appearance, nivel AAA, nuevo en WCAG 2.2) exige que el indicador de foco cubra un área al menos equivalente a un perímetro de 2px CSS alrededor del componente sin foco, Y tenga un contraste de al menos **3:1** entre los mismos píxeles en estado con foco y sin foco. Cita textual: "is at least as large as the area of a 2 CSS pixel thick perimeter of the unfocused component" y "has a contrast ratio of at least 3:1 between the same pixels in the focused and unfocused states". Fuente: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html

**Por qué el neumorphism suele fallar estos criterios**
- H6: El rasgo definitorio del neumorphism —elementos extruidos con el mismo color que el fondo, diferenciados solo por sombras claras/oscuras de bajo contraste— hace que no exista contraste real en el límite del componente, por lo que falla 1.4.11 (3:1 contra color adyacente) de forma sistemática. Fuente: https://medium.com/@xurxe/accessible-neumorphism-soft-ui-992286900bfa
- H7: Los estados de botones (presionado/activo) en neumorphism suelen distinguirse únicamente invirtiendo la dirección de la sombra (de extruido a hundido/inset), sin cambio de color ni borde, lo cual no aporta la información de estado exigida por 1.4.11 para usuarios con baja visión. Fuente: https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28
- H8: El texto colocado directamente sobre la superficie neumórfica (mismo tono que el fondo) frecuentemente cae por debajo del mínimo 4.5:1 de 1.4.3, dejando a usuarios de baja visión sin poder identificar qué es interactivo. Fuente: https://builtin.com/articles/neumorphism-accessibility

**Técnicas documentadas para mantener accesible un diseño neumórfico**
- H9: Añadir un borde sutil (frecuentemente 1px) en un tono más claro u oscuro, alineado con la dirección de la sombra, para reforzar visualmente el límite del componente sin abandonar el aspecto suave. Fuente: https://codefronts.com/design-styles/css-neumorphism/accessible-neumorphism-that-passes-contrast/
- H10: Usar colores de acento (mayor contraste que el resto de la paleta) de forma selectiva en elementos interactivos importantes, y para indicar cambios de estado (activo/hover/seleccionado), en vez de depender solo de la sombra. Fuente: https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28
- H11: Colocar el texto sobre una superficie de mayor contraste (no directamente sobre el panel neumórfico de bajo contraste) como técnica de mitigación documentada. Fuente: https://builtin.com/articles/neumorphism-accessibility
- H12: Para el estado presionado, invertir ambas sombras a "inset" (hundido) como metáfora física de pulsado — técnica documentada, pero por sí sola no basta para cumplir 1.4.11 si no hay además cambio de color o borde (ver H7). Fuente: https://uxdesign.cc/neumorphism-can-we-make-it-more-accessible-15be5fe2ef28

**Herramientas públicas para medir contraste**
- H13: WebAIM Contrast Checker es una herramienta gratuita que muestra el ratio de contraste exacto y si pasa/falla los niveles AA y AAA para texto normal, texto grande, y también los requisitos de contraste no textual de WCAG 2.1/2.2 (1.4.11). Fuente: https://webaim.org/resources/contrastchecker/

## Vacíos
- V1: No se encontró una fuente pública oficial que dé un valor numérico específico de "compensación de brillo" o un ratio de contraste ajustado recomendado para uso bajo luz solar directa en móvil. Los artículos consultados mencionan cualitativamente que el brillo/reflejo reduce el contraste percibido, pero WCAG 2.2 no define un ratio distinto para condiciones de luz solar — los ratios de 1.4.3/1.4.11/1.4.6 son los mismos independientemente del entorno de visualización.
- V2: No se pudo verificar con una fuente primaria (W3C o estudio citable) un umbral cuantitativo específico de "cuánto" se degrada un ratio de contraste en exteriores (ej. "3.8:1 baja a 2.5:1"); esa cifra apareció solo en contenido de blog sin cita primaria, así que no se incluye como hecho verificado.
- V3: No se encontró guía específica de W3C/WCAG dedicada exclusivamente a "tamaño de pantalla móvil" como factor de contraste; los criterios de contraste son agnósticos al tamaño de pantalla o dispositivo.
- V4: No se investigó ni se afirma nada sobre paletas de color, valores hexadecimales o diseño específico de la interfaz de Works — está fuera del alcance de esta pregunta.
