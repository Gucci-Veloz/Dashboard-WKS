-- 001_areas: esquema de las cuatro áreas (oficinas, inquilinos, contratos, pagos).
-- Campos provisionales hasta conocer el Excel de Works (U-1, ver plan/DECISIONES.md).
-- 'extras' guarda en JSON (como texto) las columnas del Excel que no estén
-- previstas aquí, para conectar los datos reales sin rehacer el esquema.

CREATE TABLE oficinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    numero TEXT,
    piso TEXT,
    m2 REAL,
    estatus TEXT,
    origen_dato TEXT NOT NULL CHECK (origen_dato IN ('sintetico', 'excel', 'manual')),
    extras TEXT,
    creado_en TEXT NOT NULL DEFAULT (datetime('now')),
    actualizado_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE inquilinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titular TEXT,
    contacto TEXT,
    origen_dato TEXT NOT NULL CHECK (origen_dato IN ('sintetico', 'excel', 'manual')),
    extras TEXT,
    creado_en TEXT NOT NULL DEFAULT (datetime('now')),
    actualizado_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE contratos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oficina_id INTEGER REFERENCES oficinas(id),
    inquilino_id INTEGER REFERENCES inquilinos(id),
    inicio TEXT,
    fin TEXT,
    alerta_renovacion TEXT,
    origen_dato TEXT NOT NULL CHECK (origen_dato IN ('sintetico', 'excel', 'manual')),
    extras TEXT,
    creado_en TEXT NOT NULL DEFAULT (datetime('now')),
    actualizado_en TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE pagos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    contrato_id INTEGER REFERENCES contratos(id),
    precio REAL,
    deposito_garantia REAL,
    fecha_pago TEXT,
    forma_pago TEXT,
    estatus_pago TEXT,
    origen_dato TEXT NOT NULL CHECK (origen_dato IN ('sintetico', 'excel', 'manual')),
    extras TEXT,
    creado_en TEXT NOT NULL DEFAULT (datetime('now')),
    actualizado_en TEXT NOT NULL DEFAULT (datetime('now'))
);
