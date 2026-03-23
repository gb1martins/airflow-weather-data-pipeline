import os
import psycopg2

from pathlib import Path
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
    def __init__(self, conexao : Conexao_BD, sql_dir : Path):
        self.conexao = conexao
        self.sql_dir = sql_dir


    def inserir_linhas_bd (self):

        with open(self.sql_dir, "r" , encoding="utf-8") as f:
            insert_sql = f.read()


        with self.conexao.conn.cursor() as cur:
            cur.execute(insert_sql)
            self.conexao.conn.commit()






def executar_gold():
    #Diretório
    sql_dir= Path("/opt/airflow/sql/dml/carregar_ouro.sql")

    #Declara Objetos
    conexao = Conexao_BD()
    principal = Principal(conexao,sql_dir)

    #Executa função
    principal.inserir_linhas_bd()

    #Fecha a conexão
    conexao.fechar()

