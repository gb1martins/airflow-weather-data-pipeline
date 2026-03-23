TRUNCATE TABLE gold_clima_diario;

INSERT INTO gold_clima_diario (
    dia, cidade, estado, pais,
    temp_media, temp_min_dia, temp_max_dia,
    umidade_media, vento_medio, nuvens_media
)
SELECT
    DATE(data_evento) AS dia,
    cidade,
    estado,
    pais,
    AVG(temp)        AS temp_media,
    MIN(temp)        AS temp_min_dia,
    MAX(temp)        AS temp_max_dia,
    AVG(umidade)     AS umidade_media,
    AVG(vento_vel)   AS vento_medio,
    AVG(nuvens)  AS nuvens_media
FROM silver_clima
GROUP BY dia, cidade, estado, pais;