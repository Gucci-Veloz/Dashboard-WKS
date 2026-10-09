-- 009_persona_operador: agrega a `operador` como tercera persona, con las
-- mismas reglas que David y Grecia. SQLite no permite cambiar un CHECK, así que
-- las tres tablas se reconstruyen copiando todos sus datos. La lista debe
-- coincidir con PERSONAS en app/seguridad/personas.py.

-- Fuera de la transacción: reconstruir `cuentas` sin que las llaves de
-- enlaces_acceso y sesiones bloqueen el borrado de la tabla vieja.
PRAGMA foreign_keys = OFF;

BEGIN;

CREATE TABLE cuentas_nueva (
    persona TEXT PRIMARY KEY CHECK (persona IN ('david', 'grecia', 'operador')),
    activa INTEGER NOT NULL DEFAULT 1 CHECK (activa IN (0, 1))
);
INSERT INTO cuentas_nueva (persona, activa) SELECT persona, activa FROM cuentas;
DROP TABLE cuentas;
ALTER TABLE cuentas_nueva RENAME TO cuentas;
INSERT OR IGNORE INTO cuentas (persona) VALUES ('operador');

CREATE TABLE cambios_nueva (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creado_en TEXT NOT NULL DEFAULT (datetime('now')),
    vence_en TEXT NOT NULL,
    estado TEXT NOT NULL CHECK (estado IN ('pendiente', 'confirmado')),
    area TEXT NOT NULL CHECK (area IN ('oficinas', 'inquilinos', 'contratos', 'pagos')),
    registro_id INTEGER,
    operacion TEXT NOT NULL CHECK (operacion IN ('alta', 'modificacion', 'baja')),
    valores_anteriores TEXT NOT NULL,
    valores_nuevos TEXT NOT NULL,
    observaciones TEXT,
    solicitante TEXT NOT NULL CHECK (solicitante IN ('david', 'grecia', 'operador')),
    ejecutor TEXT NOT NULL CHECK (ejecutor IN ('david', 'grecia', 'operador', 'vania')),
    confirmado_en TEXT
);
INSERT INTO cambios_nueva (
    id, creado_en, vence_en, estado, area, registro_id, operacion,
    valores_anteriores, valores_nuevos, observaciones, solicitante, ejecutor, confirmado_en
)
SELECT
    id, creado_en, vence_en, estado, area, registro_id, operacion,
    valores_anteriores, valores_nuevos, observaciones, solicitante, ejecutor, confirmado_en
FROM cambios;
-- Conserva el contador de ids aunque se hayan borrado pendientes vencidos:
-- un cambio nuevo nunca reutiliza el número de uno anterior.
DELETE FROM sqlite_sequence WHERE name = 'cambios_nueva';
INSERT INTO sqlite_sequence (name, seq)
SELECT 'cambios_nueva', seq FROM sqlite_sequence WHERE name = 'cambios';
DROP TABLE cambios;
ALTER TABLE cambios_nueva RENAME TO cambios;
CREATE INDEX cambios_pendientes_por_registro
ON cambios (area, registro_id, estado);

CREATE TABLE preferencias_avisos_nueva (
    persona TEXT NOT NULL CHECK (persona IN ('david', 'grecia', 'operador')),
    tipo_evento TEXT NOT NULL,
    hasta TEXT,
    creado_en TEXT NOT NULL,
    actualizado_en TEXT NOT NULL,
    PRIMARY KEY (persona, tipo_evento)
);
INSERT INTO preferencias_avisos_nueva (persona, tipo_evento, hasta, creado_en, actualizado_en)
SELECT persona, tipo_evento, hasta, creado_en, actualizado_en FROM preferencias_avisos;
DROP TABLE preferencias_avisos;
ALTER TABLE preferencias_avisos_nueva RENAME TO preferencias_avisos;

COMMIT;

PRAGMA foreign_keys = ON;
