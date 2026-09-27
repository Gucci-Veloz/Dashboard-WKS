# Corrección puntual T1

Capa sobre `DASHBOARD_DESIGN_SPEC.md` y `DASHBOARD_DESIGN_REFINEMENTS_T1.md`. Si se contradicen, manda este documento. Cambia un valor del documento original: la superficie de C-01, C-02 y Procesando deja de ser `#F3F6F9` y pasa a ser el color del fondo general.

## C-01, C-02 y Procesando

Aceptada la causa detectada en código:

- No existe gradient.
- El lavado visual proviene de que la superficie del botón es más clara que el fondo y el highlight superior/izquierdo es demasiado claro.

### Ajuste

- Igualar la superficie de estos botones al color del fondo general.
- Mantener la lógica neumórfica mediante:
  - highlight superior/izquierdo;
  - sombra inferior/derecha.
- Recalibrar ambas sombras para que el relieve sea claramente visible a 390 px.
- Aumentar ligeramente la presencia de la sombra oscura.
- Si el highlight blanco puro sigue perdiéndose, usar un highlight ligeramente menos blanco en lugar de aumentar exageradamente su intensidad.

El criterio de aceptación es visual:
los botones deben percibirse claramente elevados a tamaño real, especialmente por el lado izquierdo.

## C-10

No modificar la implementación actual si ya cumple:

- contenedor con `overflow-x: auto`;
- tabla más ancha que el viewport;
- página completa sin overflow horizontal.

Generar una segunda captura móvil con la tabla desplazada horizontalmente para demostrar que el scroll pertenece únicamente a la tabla.
