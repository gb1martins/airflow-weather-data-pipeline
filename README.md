# 🌦️ Airflow Weather Data Pipeline

Pipeline de dados end-to-end desenvolvido com **Python**, **Apache Airflow**, **Docker** e **PostgreSQL** para ingestão, processamento e armazenamento de dados climáticos da API OpenWeather.

---

## 🚀 Visão Geral

Este projeto implementa um pipeline de dados seguindo a arquitetura **Medallion (Bronze, Silver e Gold)**, amplamente utilizada em engenharia de dados.

O pipeline coleta dados climáticos de capitais brasileiras, processa e disponibiliza os dados para análise.

---

## 🏗️ Arquitetura do Pipeline

```
OpenWeather API
       ↓
   🥉 Bronze (dados brutos - JSON)
       ↓
   🥈 Silver (dados tratados)
       ↓
   🥇 Gold (dados analíticos)
```

---

## ⚙️ Tecnologias Utilizadas

* Python
* Apache Airflow
* Docker & Docker Compose
* PostgreSQL
* OpenWeather API
* SQL

---

## 📂 Estrutura do Projeto

```
.
├── banco_de_dados/      # Criação das tabelas no BD(ddl)
├── dags/                # DAGs do Airflow (orquestração)
├── codigo_fonte/        # Lógica do pipeline
│   ├── ingestao/
│   └── transformacao/
├── sql/                 # Scripts SQL (DDL e DML)
├── docker-compose.yaml  # Infraestrutura
├── requirements.txt     # Dependências
├── .gitignore
└── README.md
```

---

## 📁 Estruturas geradas em tempo de execução

As pastas abaixo são criadas automaticamente durante a execução do pipeline:

```
dados/   # Camadas Bronze, Silver e Gold
logs/    # Logs do Airflow
config/  # Configurações do Airflow
```

> ⚠️ Essas pastas não são versionadas no Git.

---

## 🔄 Etapas do Pipeline

### 🥉 Bronze

* Coleta dados da API OpenWeather
* Armazena os dados brutos em formato JSON na camada Bronze
* Representa a fonte original dos dados, sem transformação

---

### 🥈 Silver

* Realiza limpeza e tratamento dos dados da camada Bronze
* Padroniza estruturas e tipos de dados
* Carrega os dados em banco PostgreSQL

---

### 🥇 Gold

* Estrutura os dados para consumo analítico
* Disponibiliza informações prontas para consultas, relatórios e dashboards

---

## ⏰ Orquestração (Airflow)

O pipeline é executado automaticamente nos seguintes horários:

* 16:00
* 16:30
* 17:00

---

## ▶️ Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/airflow-weather-data-pipeline.git
cd airflow-weather-data-pipeline
```

---

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
BD_HOST=host.docker.internal
BD_PORT=5432
BD_NOME=seu_banco
BD_USER=seu_usuario
BD_SENHA=sua_senha
CHAVE_API_OPENWEATHER=sua_chave
```

---

## 🔐 Variáveis de ambiente

O arquivo `.env` não está incluído no repositório por conter informações sensíveis.

---

### 3. Subir o ambiente

```bash
docker compose up airflow-init
docker compose up -d
```

---

### 4. Acessar o Airflow

Acesse no navegador:

```
http://localhost:8080
```

Credenciais padrão:

* usuário: airflow
* senha: airflow

---

## 📊 Monitoramento

* Interface do Airflow (Graph View)
* Logs detalhados por task
* Scheduler para execução automática

---

👨‍💻 Autor

Gabriel Auguto Martins

⭐ Sobre o Projeto

Este projeto foi desenvolvido como parte da jornada de aprendizado em Engenharia de Dados, com foco em:

Orquestração de pipelines com Airflow
Integração com APIs
Processamento de dados
Arquitetura de dados moderna (Medallion)

