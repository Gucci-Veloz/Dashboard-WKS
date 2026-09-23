# VER-02 · Verificación de la fase 1

**Ejecutada:** 2026-09-23 · 5:22 CST  
**Estado:** COMPLETA CON FALLOS

---

## Resumen ejecutivo

La fase 1 construyó correctamente la pantalla de nivel 1 y el motor del estado de atención. Todas las pruebas de las tareas **PASAN**, pero se encontró **1 FALLA** crítica en la arquitectura: múltiples APIs están abriendo SQLite directamente en lugar de usar la interfaz centralizada `app/db/`.

**Total de tareas de fase 1:** 12  
**Tareas con prueba PASA:** 12/12  
**Fallas de arquitectura:** 1

---

## Pruebas por tarea

### DAT-03 · Contrato del estado de atención

**Comando:** `python3 -c "import json,sys; [json.load(open(f)) for f in sys.argv[1:]]" contratos/estado.schema.json contratos/ejemplos/*.json`

**Resultado:** JSON válido sin errores

**Verificación:** ✅ PASA

---

### DAT-04 · Esquema de las cuatro áreas

**Comando:** `pytest tests/test_dat04_esquema.py -q`

**Resultado:**
```
....                                                                     [100%]
4 passed
```

**Verificación:** ✅ PASA

---

### INT-01 · Tabla de actividad y función para registrarla

**Comando:** `pytest tests/test_int01_actividad.py -q` (ejecutada con 6 tareas juntas)

**Verificación:** ✅ PASA

---

### INT-04 · Credencial de servicio para Vania

**Comando:** `pytest tests/test_int04_actor.py -q` (ejecutada con 6 tareas juntas)

**Verificación:** ✅ PASA

---

### DAT-05 · Interfaz de fuentes de datos y cargador

**Comando:** `pytest tests/test_dat05_fuentes.py -q` (ejecutada con 6 tareas juntas)

**Verificación:** ✅ PASA

---

### DAT-06 · Fuente sintética con dos escenarios

**Comando:** `pytest tests/test_dat06_sintetica.py -q` (ejecutada con 6 tareas juntas)

**Verificación:** ✅ PASA

---

### DAT-07 · Motor del estado de atención

**Comando:** `pytest tests/test_dat07_estado.py -q` (ejecutada con 6 tareas juntas)

**Verificación:** ✅ PASA

---

### DAT-08 · Endpoint del estado

**Comando:** `pytest tests/test_dat08_api_estado.py -q` (ejecutada con 6 tareas juntas)

**Resultado (6 tareas juntas):**
```
..............................                                                     [100%]
22 passed
```

**Verificación:** ✅ PASA

---

### UI-04 · Nivel 1: estado general

**Comando:** `pytest tests/ui/test_ui04_nivel1.py -q` (ejecutada con 4 tareas UI juntas)

**Verificación:** ✅ PASA

---

### UI-05 · Nivel 2: lo que merece atención

**Comando:** `pytest tests/ui/test_ui05_nivel2.py -q` (ejecutada con 4 tareas UI juntas)

**Verificación:** ✅ PASA

---

### UI-06 · Indicadores que explican el estado

**Comando:** `pytest tests/ui/test_ui06_indicadores.py -q` (ejecutada con 4 tareas UI juntas)

**Verificación:** ✅ PASA

---

### UI-07 · Conectar niveles 1 y 2 al servicio

**Comando:** `pytest tests/ui/test_ui07_api.py -q` (ejecutada con 4 tareas UI juntas)

**Resultado (4 tareas UI juntas):**
```
....................                                                     [100%]
20 passed
```

**Verificación:** ✅ PASA

---

## Revisión contra el handshake

### Sin KPI dominante ni `%` o `$` en el nivel 1

**Comando:** `grep -rn "\$\|%" web/nivel1/`

**Resultado:** Sin coincidencias

**Verificación:** ✅ OK

---

### En estado tranquilo no hay actividad artificial

**Prueba:** Cargar escenario tranquilo y verificar que no haya asuntos ni conclusiones falsas

**Resultado:**
- Conclusión: tranquilo
- Cantidad de asuntos: 0
- Indicadores presentes: 4 (áreas, correctos)

**Verificación:** ✅ OK

---

### El mismo orden sale en dos corridas

**Prueba:** Ejecutar el motor de estado dos veces con la misma fecha y escenario

**Resultado:**
- Primera corrida: contratos (contrato-4) → pagos (pago-8) → inquilinos (inquilino-9)
- Segunda corrida: contratos (contrato-4) → pagos (pago-8) → inquilinos (inquilino-9)
- **Orden DETERMINISTA:** sí

**Verificación:** ✅ OK

---

### Todo es sintético (sin datos reales)

**Comandos ejecutados con base temporal:**
```
WORKS_DB=/tmp/claude-verif/works.db python -m app.db.migrar
WORKS_DB=/tmp/claude-verif/works.db python -m app.fuentes.cargar --fuente sintetica --escenario con_atencion
```

**Resultados:**
```
sqlite3 /tmp/claude-verif/works.db "SELECT count(*) FROM oficinas WHERE origen_dato<>'sintetico';"
→ 0 ✓

sqlite3 /tmp/claude-verif/works.db "SELECT count(*) FROM inquilinos WHERE origen_dato<>'sintetico';"
→ 0 ✓

sqlite3 /tmp/claude-verif/works.db "SELECT count(*) FROM contratos WHERE origen_dato<>'sintetico';"
→ 0 ✓

sqlite3 /tmp/claude-verif/works.db "SELECT count(*) FROM pagos WHERE origen_dato<>'sintetico';"
→ 0 ✓
```

**Verificación:** ✅ OK (todos los registros tienen origen_dato='sintetico')

---

## ⚠️ FALLA CRÍTICA: SQLite abierto fuera de `app/db/`

**Regla del handshake:** "FastAPI es la única capa que toca SQLite. Solo `app/db/` abre la base."

**Comando de verificación:** `grep -rn "sqlite3" app --include=*.py | grep -v "^app/db/"`

**Resultado:** FALLA ENCONTRADA

**Archivos problemáticos:**
1. `app/api/oficinas.py:1` – Import de sqlite3
2. `app/api/oficinas.py:25-27` – Función `_conectar_con_filas()` que abre conexión directamente
3. `app/api/inquilinos.py:1` – Import de sqlite3
4. `app/api/inquilinos.py:22-24` – Función `_conectar_con_filas()` que abre conexión directamente
5. `app/api/estado.py:1` – Import de sqlite3
6. `app/api/estado.py:15` – Apertura directa de conexión
7. `app/api/contratos.py:1` – Import de sqlite3
8. `app/api/contratos.py:27-29` – Función `_conectar_con_filas()` que abre conexión directamente
9. `app/api/actividad.py:1` – Import de sqlite3
10. `app/api/actividad.py:29` – Apertura directa de conexión
11. `app/api/pagos.py:1` – Import de sqlite3
12. `app/api/pagos.py:35-37` – Función `_conectar_con_filas()` que abre conexión directamente

**Impacto:** Viola la arquitectura de capa única de acceso a BD. Complica futuros cambios de base de datos y distribuye la lógica de conexión.

**Recomendación:** Centralizar todas las conexiones en `app/db/conexion.py` y exponerlas como dependencias de FastAPI. Las APIs deben importar de `app/db` únicamente.

---

## Resumen de resultados

| Tarea | Tipo | Estado | Detalle |
|-------|------|--------|---------|
| DAT-03 | Contrato | PASA | JSON válido |
| DAT-04 | Esquema | PASA | 4/4 pruebas |
| INT-01 | Actividad | PASA | Incluido en 22/22 |
| INT-04 | Credencial | PASA | Incluido en 22/22 |
| DAT-05 | Fuentes | PASA | Incluido en 22/22 |
| DAT-06 | Sintética | PASA | Incluido en 22/22 |
| DAT-07 | Motor estado | PASA | Incluido en 22/22 |
| DAT-08 | Endpoint | PASA | Incluido en 22/22 |
| UI-04 | Nivel 1 | PASA | Incluido en 20/20 |
| UI-05 | Nivel 2 | PASA | Incluido en 20/20 |
| UI-06 | Indicadores | PASA | Incluido en 20/20 |
| UI-07 | Conectar API | PASA | Incluido en 20/20 |
| **Total pruebas de tareas** | — | **PASA** | **42/42** |

| Punto de revisión | Estado | Detalle |
|------------------|--------|---------|
| Sin KPI ni símbolos | ✅ OK | No hay `%` ni `$` en nivel 1 |
| Sin actividad artificial | ✅ OK | Tranquilo = 0 asuntos |
| Orden determinista | ✅ OK | Dos corridas = mismo orden |
| Datos sintéticos | ✅ OK | 100% origen_dato='sintetico' |
| Solo app/db abre SQLite | ❌ FALLA | 12 archivos abren directamente |

---

## Conclusión

**Fase 1 funcional:** La pantalla de nivel 1, el motor de estado y la conexión al servicio funcionan correctamente. Todas las pruebas pasan.

**Arquitectura comprometida:** La violación crítica de que múltiples APIs abren SQLite directamente debe resolverse antes de fase 2, para evitar el caos de dependencias durante la escalada.

**Siguiente:** Resolver la falla de arquitectura o documentar por qué es aceptable. Luego liberar fase 2.
