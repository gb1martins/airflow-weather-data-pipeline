from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime
import sys
from pathlib import Path

sys.path.append("/opt/airflow")

from codigo_fonte.ingestao.api_openweather import executar_bronze
from codigo_fonte.transformacao.bronze_para_silver import executar_silver
from codigo_fonte.transformacao.silver_para_gold import executar_gold
def criar_dag(nome_dag, cron):
    with DAG(
        dag_id=nome_dag,
        start_date=datetime(2024,1,1),
        schedule=cron,
        catchup=False,
        max_active_runs=1,
        tags=["clima","bronze-silver-gold"]
    ) as dag:

        bronze_task = PythonOperator(
            task_id="bronze",
            python_callable=executar_bronze
        )

        silver_task = PythonOperator(
            task_id="silver",
            python_callable=executar_silver
        )

        gold_task = PythonOperator(
            task_id="gold",
            python_callable=executar_gold
        )

        bronze_task >> silver_task >> gold_task

    return dag


dag_19 = criar_dag("pipeline_clima_19", "0 19 * * *")
dag_1930 = criar_dag("pipeline_clima_1930", "30 19 * * *")
dag_20 = criar_dag("pipeline_clima_20", "0 20 * * *")

globals()["pipeline_clima_19"] = dag_19
globals()["pipeline_clima_1930"] = dag_1930
globals()["pipeline_clima_20"] = dag_20