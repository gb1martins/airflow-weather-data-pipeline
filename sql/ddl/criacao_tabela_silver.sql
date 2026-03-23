CREATE TABLE IF NOT EXISTS silver_clima (
    id               BIGSERIAL PRIMARY KEY,
    data_evento      TIMESTAMP NOT NULL,
    tempo_de_ingestao TIMESTAMP DEFAULT NOW(),

    cidade           TEXT NOT NULL,
    estado           TEXT,
    pais             TEXT,

    lat              NUMERIC(9,6),
    lon              NUMERIC(9,6),

    temp             NUMERIC(5,2),
    sensacao_termica NUMERIC(5,2),
    temp_min_local   NUMERIC(5,2),   
    temp_max_local   NUMERIC(5,2),

    umidade          INT,
    pressao          INT,

    vento_vel        NUMERIC(5,2),
    vento_dir        INT,

    nuvens       INT,

    clima_pri       TEXT,
    clima_desc       TEXT,

    visibilidade     INT,

    nascer_do_sol          TIMESTAMP,
    por_do_sol           TIMESTAMP
);

-- Índices úteis
CREATE INDEX IF NOT EXISTS idx_silver_clima_evento
  ON silver_clima (data_evento);

CREATE INDEX IF NOT EXISTS idx_silver_clima_cidade
  ON silver_clima (cidade, estado);