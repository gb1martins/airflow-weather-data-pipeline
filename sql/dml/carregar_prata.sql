INSERT INTO silver_clima (
            data_evento, cidade, estado, pais, lat, lon,
            temp, sensacao_termica, temp_min_local, temp_max_local,
            umidade, pressao, vento_vel, vento_dir, nuvens,
            clima_pri, clima_desc, visibilidade, nascer_do_sol, por_do_sol
        ) VALUES (
            %(data_evento)s, %(cidade)s, %(estado)s, %(pais)s, %(lat)s, %(lon)s,
            %(temp)s, %(sensacao_termica)s, %(temp_min_local)s, %(temp_max_local)s,
            %(umidade)s, %(pressao)s, %(vento_vel)s, %(vento_dir)s, %(nuvens)s,
            %(clima_pri)s, %(clima_desc)s, %(visibilidade)s, %(nascer_do_sol)s, %(por_do_sol)s
        );
        