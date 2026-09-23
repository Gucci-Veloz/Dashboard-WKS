# Siguientes pasos · Vania y el Dashboard de Works

Fecha: 2026-09-20
Fuente: cierre de `/grill-me` sobre `handshake_vania_dashboard.md` (status: `complete, grilled`)

Este documento no reabre decisiones de producto. Es la traducción de "ya está definido, ¿ahora qué?" a acciones concretas.

## Paso inmediato: pasar a planificación

```
/make-plan handshake_vania_dashboard.md
```

Esto convierte el brief cerrado en un plan por fases. Después:

```
/do
```

ejecuta ese plan con subagentes.

**Regla que viene del grilling y aplica también a planificación y construcción:**

> Encontrar una posible mejora no autoriza a convertirla en requisito.

Antes de que planificación o implementación abran una decisión nueva de producto, debe pasar este filtro:

> ¿Este punto impide construir o planificar correctamente la idea ya definida?

Si la respuesta es no, se resuelve en su propia etapa (UX, implementación, planificación) y no se convierte en una decisión nueva del handshake.

## En paralelo: conseguir el Excel real de Works

Es la única dependencia de terceros del proyecto, y quedó declarada explícitamente como **bloqueante del lanzamiento, no del desarrollo**:

- No bloquea seguir construyendo lo que depende del desarrollador.
- Sí bloquea el inicio de la prueba operativa real con David y Grecia.

El Google Sheet preliminar que existe hoy es solo un placeholder. No se convierte en fuente de verdad, y no se inventan datos.

## Por dónde empezar a construir

**Recomendación: empezar por la pantalla de nivel 1 del Dashboard, no por el modelo de datos.**

Razón: esa pantalla concentra toda la identidad del producto (neumorphism, calma, la frase en lenguaje humano, el principio "no des la hora si no te la piden"). Es lo más fácil de arruinar y lo único que un refactor posterior no puede arreglar. El CRUD de las cuatro áreas es trabajo ya conocido; esta pantalla no.

Se puede construir y vivir con ella varios días usando **datos sintéticos marcados explícitamente como tales**, sin esperar al Excel real.

Si al desarrollador no le dan ganas de abrirla, es señal de que a David tampoco se las va a dar.

## Observaciones enviadas a etapas posteriores

Registradas durante el grilling, no son decisiones pendientes del producto. Se anotan para que quien llegue a cada etapa las tenga presentes:

- **UX:** posición exacta del rastro de Vania en la interfaz. El boceto conceptual original mostraba un contador de movimientos; revisar contra el principio "no des la hora si no te la piden". El boceto en el handshake no es vinculante.
- **UX:** cómo se produce visualmente el efecto de sorpresa, dado que el Dashboard se inclina hacia la calma en vez del impacto visual.
- **UX:** tratamiento visual de las correcciones humanas sobre acciones de Vania.
- **Planificación:** cómo se observará, al cierre de la semana de prueba, la señal de adopción de Grecia (uso autónomo y recurrente ante necesidades reales, no uso diario).
- **Riesgo conocido:** una ventana de prueba que caiga en un tramo tranquilo del ciclo mensual de Works puede producir poca señal, sin que eso signifique que el producto falló.
- **Riesgo conocido:** un error de Vania que nadie note durante la semana de prueba puede costar más que la ausencia de la función.

## Bloqueadores reales para pasar a planificación

**Ninguno.** Nada impide elaborar el plan hoy. Los pendientes grandes que quedan (autenticación, dónde vive la lógica de "estado de atención", qué documento produce la capacidad heroica) son cosas que el planner debe **proponer**, no cosas que el planner necesita resueltas de antemano para empezar.

## Referencia

Documento fuente: `handshake_vania_dashboard.md`, en el mismo directorio. Es la fuente de verdad de producto; este archivo solo traduce su cierre en acción.
