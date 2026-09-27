-- 003_preferencias_avisos: silencios por persona y avisos emitidos una sola vez.

CREATE TABLE preferencias_avisos (
    persona TEXT NOT NULL CHECK (persona IN ('david', 'grecia')),
    tipo_evento TEXT NOT NULL,
    hasta TEXT,
    creado_en TEXT NOT NULL,
    actualizado_en TEXT NOT NULL,
    PRIMARY KEY (persona, tipo_evento)
);

CREATE TABLE avisos_emitidos (
    persona TEXT NOT NULL,
    asunto_id TEXT NOT NULL,
    tipo_evento TEXT NOT NULL,
    huella TEXT NOT NULL,
    avisado_en TEXT NOT NULL,
    PRIMARY KEY (persona, asunto_id)
);

CREATE INDEX idx_avisos_emitidos_persona_tipo
    ON avisos_emitidos (persona, tipo_evento);
