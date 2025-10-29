import httpx
import requests

from queries import pipefy
from src.config.settings import Settings


class pipefyClient:
    BASE_URL = "https://api.pipefy.com/graphql"

    def __init__(self):
        self.api_token = Settings.PIPEFY_API_KEY
        if not self.api_token:
            raise ValueError("A variável PIPEFY_API_KEY não foi configurada.")

        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    def create_card(self, pipe_id: str, fields: list[dict]):
        query = pipefy.card_creator()
        variables = {"input": {"pipe_id": pipe_id, "fields_attributes": fields}}

        response = requests.post(
            self.BASE_URL, headers=self.headers, json={"query": query, "variables": variables}
        )

        # 💬 Debug: exibe status e resposta completa
        print("\n🔍 [DEBUG] STATUS:", response.status_code)
        print("🔍 [DEBUG] RESPONSE:", response.text)

        if response.status_code != 200:
            raise Exception(f"Erro HTTP {response.status_code}: {response.text}")

        data = response.json()

        # ⚠️ Trata erros do GraphQL
        if "errors" in data:
            raise Exception(f"Erro GraphQL: {data['errors']}")

        # 🔒 Garante que não quebre se algo vier vazio
        card_data = (
            data.get("data", {})
            .get("createCard", {})
            .get("card", None)
        )

        if card_data is None:
            raise Exception(f"Erro: resposta inesperada da API Pipefy: {data}")

        return card_data

    async def update_card(self, card_id: str, fields: list[dict]):
        query = pipefy.card_updator()
        variables = {"input": {"id": card_id, "fields_attributes": fields}}
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.BASE_URL, headers=self.headers, json={"query": query, "variables": variables}
            )

        if response.status_code != 200:
            raise Exception(f"Erro ao atualizar card: {response.text}")

        data = response.json()
        return data.get("data", {}).get("updateCard", {}).get("card")