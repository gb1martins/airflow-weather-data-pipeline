CREATE TABLE IF NOT EXISTS gold_clima_diario (
    dia             DATE,
    cidade          TEXT,
    estado          TEXT,
    pais            TEXT,

    temp_media      NUMERIC(5,2),
    temp_min_dia    NUMERIC(5,2),
    temp_max_dia    NUMERIC(5,2),

    umidade_media   NUMERIC(5,2),
    vento_medio     NUMERIC(5,2),
    nuvens_media    NUMERIC(5,2)
    
);