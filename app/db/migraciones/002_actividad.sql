-- 002_actividad: rastro de lo que hace Vania y el Dashboard.
-- Distingue 'solicitada' (confirma algo que alguien pidió) de 'detectada'
-- (Vania lo encontró sin que nadie preguntara) y 'automatica' (ver PLAN.md, INT-01).

CREATE TABLE actividad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    momento TEXT NOT NULL DEFAULT (datetime('now')),
    actor TEXT NOT NULL CHECK (actor IN ('vania', 'dashboard', 'sistema')),
    persona TEXT,
    tipo TEXT NOT NULL CHECK (tipo IN ('solicitada', 'detectada', 'automatica')),
    accion TEXT NOT NULL,
    area TEXT,
    referencia TEXT,
    resumen TEXT NOT NULL,
    origen_dato TEXT NOT NULL CHECK (origen_dato IN ('sintetico', 'real'))
);
