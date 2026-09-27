La dirección visual actual queda **APROBADA**.

No rediseñes.
No cambies la geometría base.
No cambies anchos, alturas, radios, alineaciones ni estructura.
No sustituyas iconos ni alteres funcionalidad.

Esta iteración es únicamente de **pulido óptico final**.

## 1. C-04 · Campo hundido

La dirección es correcta.

Refina ligeramente la cavidad para que alcance la misma calidad óptica que los controles elevados.

Ajusta únicamente:

- `inset shadow`;
- highlight interior arriba/izquierda;
- sombra interior abajo/derecha;
- transición entre superficie y cavidad.

Debe verse un poco más profundo, pero seguir limpio.

No añadir borde convencional.
No oscurecerlo agresivamente.

---

## 2. C-08 · Overlay

El problema anterior ya quedó corregido.

Ahora mejora únicamente su acabado:

- un poco más de aire interior;
- mejor balance entre contenido y bordes;
- profundidad N3 ligeramente más refinada;
- mantener la silueta limpia y simétrica.

No hacerlo más pesado.
No añadir otra capa.
No cambiar su estructura.

---

## 3. C-10 · Conjunto de registros

Funcionalmente ya está correcto.

Haz únicamente un refinamiento visual para que no se sienta como una zona ajena al resto del sistema.

Mantener:

- tabla plana;
- scroll horizontal interno;
- sin tarjetas por fila;
- sin neumorfismo excesivo.

Mejorar sutilmente:

- jerarquía del encabezado;
- ritmo vertical;
- separación entre filas;
- integración con la superficie general.

Debe seguir siendo el componente más sobrio del conjunto.

---

## 4. Consistencia óptica global

Haz una última pasada visual sobre:

- sombras;
- highlights;
- separación entre superficies;
- pesos iconográficos;
- ritmo vertical.

No cambies ningún componente que ya esté bien únicamente para “hacer algo”.

Solo corrige diferencias perceptibles.

---

## 5. Protección contra regresiones

No modificar:

- C-01;
- C-02;
- Procesando;
- Éxito;
- Error;
- Deshabilitado;
- C-03;
- C-05;
- C-06;
- C-07;
- C-09;

salvo microajuste estrictamente necesario para mantener consistencia óptica.

No cambies:

- textos;
- acciones;
- funcionalidad;
- flujos;
- backend.

---

## 6. Criterio de aceptación

Genera nueva evidencia a `390px`.

La iteración solo se acepta si:

- C-04 se percibe ligeramente más profundo;
- C-08 se siente más refinado sin cambiar su estructura;
- C-10 se integra mejor visualmente sin perder sobriedad;
- no existe ninguna regresión visible en los componentes ya aprobados.

No generes informe adicional.
No reevalúes el diseño completo.
No reconstruyas.

Pulir, renderizar, comparar y entregar evidencia.
