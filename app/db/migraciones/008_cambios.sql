-- 008_cambios: pendientes, historial y fuente del reporte diario.
CREATE TABLE cambios (
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
    solicitante TEXT NOT NULL CHECK (solicitante IN ('david', 'grecia')),
    ejecutor TEXT NOT NULL CHECK (ejecutor IN ('david', 'grecia', 'vania')),
    confirmado_en TEXT
);

CREATE INDEX cambios_pendientes_por_registro
ON cambios (area, registro_id, estado);
