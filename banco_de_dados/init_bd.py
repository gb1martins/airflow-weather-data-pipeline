import os
import psycopg2
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

class ConexaoBD:
    def __init__(self):
        self.host = os.getenv("BD_HOST")
        self.port = os.getenv("BD_PORT")
        self.dbname = os.getenv("BD_NOME")
        self.user = os.getenv("BD_USER")
        self.password = os.getenv("BD_SENHA")

        self.conn = psycopg2.connect(   
            host=self.host,
            port=self.port,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
        )

    def fechar(self):
        self.conn.close()
        print("🔌 Conexão com o banco encerrada.")

class ExecutorDDL:
    def __init__(self, conexao: ConexaoBD, ddl_path_silver: str, ddl_path_gold : str):
        self.conexao = conexao
        self.ddl_path_silver = ddl_path_silver
        self.ddl_path_gold = ddl_path_gold

    def executar_silver(self):
        with open(self.ddl_path_silver, "r", encoding="utf-8") as f:
            ddl_silver = f.read()

        with self.conexao.conn:
            with self.conexao.conn.cursor() as cur:
                cur.execute(ddl_silver)

        print("DDL executado com sucesso da tabela silver!")

    
    def executar_gold(self):
        with open(self.ddl_path_gold, "r", encoding="utf-8") as f:
            ddl_gold = f.read()

        with self.conexao.conn:
            with self.conexao.conn.cursor() as cur:
                cur.execute(ddl_gold)

        print("DDL executado com sucesso da tabela gold!")


if __name__ == "__main__":
    conexao = ConexaoBD()
    executor = ExecutorDDL(conexao, r"C:\Users\x\Desktop\Engenharia de Dados - MBA\Projetos - Estudo\Pipeline de Dados - Clima\sql\ddl\criacao_tabela_silver.sql", r"C:\Users\x\Desktop\Engenharia de Dados - MBA\Projetos - Estudo\Pipeline de Dados - Clima\sql\ddl\criacao_tabela_gold.sql")
    #Executa a criação da tabela silvar
    executor.executar_silver()
    #Executa a criação da tabela gold
    executor.executar_gold()
    #Fecha conexão
    conexao.fechar()
            


