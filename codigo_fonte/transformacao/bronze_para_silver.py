import os
import json
from pathlib import Path
from datetime import datetime, timezone

import psycopg2
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()


class Conexao_BD:
    def __init__(self):
        self.host = os.getenv("BD_HOST")
        self.port = os.getenv("BD_PORT")
        self.nome = os.getenv("BD_NOME")
        self.user = os.getenv("BD_USER")
        self.senha = os.getenv("BD_SENHA")

        self.conn = psycopg2.connect(
            host = self.host,
            port = self.port,
            dbname = self.nome,
            user = self.user,
            password = self.senha
        )

        print("🔌 Conexão com o banco iniciada.")

    def fechar(self):
        self.conn.close()
        print("🔌 Conexão com o banco encerrada.")

class Principal:
    def __init__(self, conexao: Conexao_BD, bronze_dir: Path, processado_dir: Path, sql_dir : Path):
        self.conexao = conexao
        self.bronze_dir = bronze_dir
        self.processado_dir = processado_dir
        self.sql_dir = sql_dir

    def ler_arquivos_json(self):
        self.bronze_dir.mkdir(exist_ok=True)

        files = list(self.bronze_dir.glob("*.json"))
        if not files:
            print("ℹ️ Nenhum JSON encontrado em:", self.bronze_dir.resolve())
            return

        rows = []
        for path in files:
            with open(path, "r", encoding="utf-8") as f:
                payload = json.load(f)

                estado = self.extrair_estado_do_arquivo(path.name)
                row = self.extrair_silver_linha(payload, estado)
                rows.append(row)

        try:
            self.inserir_linhas_bd(rows)
            # Move arquivos processados
            for path in files:
                path.rename(self.processado_dir / path.name)

            print(f"✅ Inseridos {len(rows)} registros na silver_clima.")
            print("📁 Arquivos movidos para:", self.processado_dir.resolve())
        finally:    
            self.conexao.fechar()

    def extrair_estado_do_arquivo(self, nome_do_arquivo: str) -> str:
        return nome_do_arquivo.split("_", 1)[0].upper()

    def extrair_silver_linha(self, payload: dict, estado: str | None) -> dict:
        return {
            "data_evento": datetime.fromtimestamp(payload["dt"], tz=timezone.utc),
            "cidade": payload["name"],
            "estado": estado,
            "pais": payload["sys"]["country"],
            "lat": payload["coord"]["lat"],
            "lon": payload["coord"]["lon"],
            "temp": payload["main"]["temp"],
            "sensacao_termica": payload["main"]["feels_like"],
            "temp_min_local": payload["main"].get("temp_min"),
            "temp_max_local": payload["main"].get("temp_max"),
            "umidade": payload["main"]["humidity"],
            "pressao": payload["main"]["pressure"],
            "vento_vel": payload["wind"]["speed"],
            "vento_dir": payload["wind"].get("deg"),
            "nuvens": payload["clouds"]["all"],
            "clima_pri": payload["weather"][0]["main"],
            "clima_desc": payload["weather"][0]["description"],
            "visibilidade": payload.get("visibility"),
            "nascer_do_sol": datetime.fromtimestamp(payload["sys"]["sunrise"], tz=timezone.utc),
            "por_do_sol": datetime.fromtimestamp(payload["sys"]["sunset"], tz=timezone.utc),
        }

    def inserir_linhas_bd(self, rows: list):
        with open(self.sql_dir, "r", encoding="utf-8") as f:
            insert_sql = f.read()

        with self.conexao.conn.cursor() as cur:
            cur.executemany(insert_sql, rows)
            self.conexao.conn.commit()

    


def executar_silver():
    #Diretório
    BRONZE_DIR = Path("/opt/airflow/dados/bronze/clima")
    bronze_dir="/opt/airflow/dados/bronze/clima/processados"
    PROCESSADO_DIR = Path("/opt/airflow/dados/bronze/clima/processados")
    SQL_DIR = Path("/opt/airflow/sql/dml/carregar_prata.sql")
    #Declara Objetos
    conexao = Conexao_BD()
    principal = Principal(conexao,BRONZE_DIR,PROCESSADO_DIR,SQL_DIR)

    #Executa função dos objetos
    principal.ler_arquivos_json()