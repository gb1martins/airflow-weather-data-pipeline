import os
import json
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

# carrega .env
load_dotenv()


class IngestaoConfig:
    def __init__(
        self,
        estados: list[str],
        bronze_dir: str = "/opt/airflow/dados/bronze/clima",
        country: str = "BR",
        timeout: int = 30,
    ):
        self.estados = estados
        self.bronze_dir = bronze_dir
        self.country = country
        self.timeout = timeout


class ClienteTempoAberto:
    def __init__(self, api_key: str | None = None, timeout: int = 30):
        self.api_key = api_key or os.getenv("CHAVE_API_OPENWEATHER")
        if not self.api_key:
            raise ValueError("CHAVE_API_OPENWEATHER não encontrada no .env")

        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.timeout = timeout

    def get_tempo(self, city: str, country: str = "BR") -> dict:
        params = {
            "q": f"{city},{country}",
            "appid": self.api_key,
            "units": "metric",
            "lang": "pt_br",
        }
        resp = requests.get(self.base_url, params=params, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()


class EstadoTempoIngestao:
    def __init__(
        self,
        client: ClienteTempoAberto,
        estados_cidades: dict[str, list[str]],
        config: IngestaoConfig,
    ):
        self.client = client
        self.estados_cidades = estados_cidades
        self.bronze_dir = Path(config.bronze_dir)
        self.country = config.country
        self.estados_para_rodar = config.estados

    def ingest(self):
        for state_code in self.estados_para_rodar:
            self._ingest_state(state_code)

    def _ingest_state(self, state_code: str):
        cities = self.estados_cidades.get(state_code)
        if not cities:
            raise ValueError(f"Estado '{state_code}' não configurado.")

        for city in cities:
            print(f" Buscando clima de {city}/{state_code}...")
            data = self.client.get_tempo(city, self.country)
            self._save_bronze(data, state_code, city)

    def _save_bronze(self, data: dict, state_code: str, city: str):
        self.bronze_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        filename = f"{state_code.lower()}_{city.lower().replace(' ', '_')}_{ts}.json"
        path = self.bronze_dir / filename

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f" Salvo em: {path}")


def executar_bronze():
    ESTADOS_CIDADES = {
    "AC": ["Rio Branco"],
    "AL": ["Maceio"],
    "AP": ["Macapa"],
    "AM": ["Manaus"],
    "BA": ["Salvador"],
    "CE": ["Fortaleza"],
    "DF": ["Brasilia"],
    "ES": ["Vitoria"],
    "GO": ["Goiania"],
    "MA": ["Sao Luis"],
    "MT": ["Cuiaba"],
    "MS": ["Campo Grande"],
    "MG": ["Belo Horizonte"],
    "PA": ["Belem"],
    "PB": ["Joao Pessoa"],
    "PR": ["Curitiba"],
    "PE": ["Recife"],
    "PI": ["Teresina"],
    "RJ": ["Rio de Janeiro"],
    "RN": ["Natal"],
    "RS": ["Porto Alegre"],
    "RO": ["Porto Velho"],
    "RR": ["Boa Vista"],
    "SC": ["Florianopolis"],
    "SP": ["Sao Paulo"],
    "SE": ["Aracaju"],
    "TO": ["Palmas"],
}

    config = IngestaoConfig(
        estados=["AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"],
        bronze_dir="/opt/airflow/dados/bronze/clima",
        country="BR",
        timeout=30,
    )

    client = ClienteTempoAberto(timeout=config.timeout)
    ingestor = EstadoTempoIngestao(client, ESTADOS_CIDADES, config)

    ingestor.ingest()