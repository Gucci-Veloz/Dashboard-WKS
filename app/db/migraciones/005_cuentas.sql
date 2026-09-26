-- 005_cuentas: acceso por enlace de un solo uso y sesiones por dispositivo.

CREATE TABLE cuentas (
    persona TEXT PRIMARY KEY CHECK (persona IN ('david', 'grecia')),
    activa INTEGER NOT NULL DEFAULT 1 CHECK (activa IN (0, 1))
);

INSERT OR IGNORE INTO cuentas (persona) VALUES ('david');
INSERT OR IGNORE INTO cuentas (persona) VALUES ('grecia');

CREATE TABLE enlaces_acceso (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona TEXT NOT NULL REFERENCES cuentas(persona),
    token_hash TEXT NOT NULL UNIQUE,
    creado_en TEXT NOT NULL,
    vence_en TEXT NOT NULL,
    usado_en TEXT
);

CREATE TABLE sesiones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona TEXT NOT NULL REFERENCES cuentas(persona),
    token_hash TEXT NOT NULL UNIQUE,
    creado_en TEXT NOT NULL,
    vence_en TEXT NOT NULL,
    revocada_en TEXT
);
