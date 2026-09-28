# Datos sintéticos

Los datos que genera `app/fuentes/sintetica.py` son inventados para desarrollo. No se parecen a propósito a los datos reales de Works: los nombres, números de oficina y montos son de ejemplo, no una imitación disimulada.

Toda fila que produce esta fuente lleva `origen_dato = 'sintetico'`, y cada titular se llama "Titular Sintético NN" para que sea imposible confundirlo con un dato real (regla 3 de `plan/PLAN.md`).

## Escenarios

- `tranquilo`: ninguna oficina, contrato, pago o inquilino requiere atención.
- `con_atencion`: reproduce los tres tipos de asunto de `contratos/ejemplos/estado-atencion.json` (DAT-03):
  - un contrato que se acerca a su fecha de vencimiento (vence en 12 días desde "hoy"),
  - un pago pendiente,
  - un inquilino con el contacto incompleto.

"Hoy" se puede fijar al construir la fuente (`FuenteSintetica(fecha_hoy=...)`), para que las pruebas no dependan de la fecha real.

## Cargar

```
python -m app.fuentes.cargar --fuente sintetica --escenario tranquilo
python -m app.fuentes.cargar --fuente sintetica --escenario con_atencion
```
