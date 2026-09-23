# Contrato del estado de atención

`estado.schema.json` es la forma que comparten el Dashboard y Vania para hablar del mismo estado de Works: un solo cerebro, dos superficies (ver `handshake_vania_dashboard.md` y D-3 en `plan/DECISIONES.md`).

## Las frases son provisionales

El texto exacto de `conclusion.frase`, `asuntos[].frase`, `asuntos[].por_que_importa` e `indicadores[].frase_corta` en los ejemplos de esta carpeta es solo ilustrativo. La redacción definitiva vive en un solo lugar (`app/estado/redaccion.py`, DAT-07) para poder cambiarla sin tocar el resto del sistema. No se debe copiar el texto de estos ejemplos como si fuera la redacción final.

## Ejemplos

- `ejemplos/estado-tranquilo.json`: nada requiere atención. `asuntos` queda vacío.
- `ejemplos/estado-atencion.json`: reproduce los tres asuntos que usará la fuente sintética `con_atencion` (DAT-06).

Los dos ejemplos llevan `"origen_datos": "sintetico"` porque no hay datos reales todavía (el Excel de Works no existe, ver `SCAVENGE-Vania-Dashboard.md`).

## Reglas del esquema

- `conclusion` no lleva `%` ni `$`: es una frase humana con una cantidad, no un KPI (regla 9 de `plan/PLAN.md`).
- Ningún `indicador` se marca como principal: todos tienen el mismo peso.
- Las fechas no se escriben en formato `dd/mm/aaaa` dentro de las frases; se redactan como las diría una persona ("vence en 12 días").
