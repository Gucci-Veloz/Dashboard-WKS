# T1g · Delta única: silueta de C-08

T1f queda aprobado salvo C-08. Todo lo demás está BLOQUEADO (mismas reglas que T1f).

## Problema observado en `evidencia/UI-21/componentes-390.png` (tras T1f)
1. Sobre el borde superior de C-08 se ve un segundo contorno curvo: otra capa o sombra se asoma detrás del modal (doble silueta).
2. El borde inferior de C-08 no se distingue: el modal se funde con C-10, que está debajo.

## Acción
- Inspecciona el DOM y los estilos computados de C-08 y de sus padres (pseudoelementos, wrappers, `box-shadow`, `overflow`, `transform`, márgenes negativos, fondos).
- Elimina la causa raíz de la doble silueta. No la tapes con parches del color del fondo.
- C-08 debe leerse como UNA sola superficie elevada (N3), con contorno continuo en los cuatro lados y separación visible respecto de C-10.

## Gates
- FAIL-A: persiste cualquier segundo contorno o capa asomada en C-08.
- FAIL-B: el borde inferior de C-08 no se distingue de C-10.
- FAIL-C: cualquier cambio fuera de C-08 (o regresión en los controles aprobados).

## Validación
Nueva captura `evidencia/UI-21/componentes-390.png`, pruebas existentes en verde y contraste en 0. Sin documentos de comparación.
