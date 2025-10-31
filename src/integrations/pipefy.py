from typing import Any

import requests
from src.config.settings import Settings
from queries import pipefy

class pipefyClient:
    BASE_URL = "https://api.pipefy.com/graphql"

    def __init__(self):
        self.api_token = Settings.PIPEFY_API_KEY
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }

    async def create_card(self, pipe_id: str, fields: dict[str, Any]):
        query = pipefy.card_creator()
        variables = {"input": {"pipe_id": pipe_id, "fields_attributes": fields['fields_attributes']}}
        print(f"jesus: {variables}")
        response = requests.post(self.BASE_URL, headers=self.headers, json={"query": query, "variables": variables})
        data = response.json()
        if "errors" in data:
            raise Exception(f"Erro GraphQL: {data['errors']}")
        return data["data"]["createCard"]["card"]



    async def update_card(self, card_id: str, fields: list[dict[str, str]]):
        query = pipefy.card_updator()
        variables = {
            "input": {
                "nodeId": card_id,
                "values": fields  # A lista de campos agora se chama "values"
            }
        }
        response = requests.post(self.BASE_URL, headers=self.headers, json={"query": query, "variables": variables})
        data = response.json()
        if "errors" in data:
            raise Exception(f"Erro GraphQL: {data['errors']}")
        return data["data"]["updateCard"]["card"]

    def find_card_by_email(self, pipe_id: str, email: str):
        """
        Busca card existente pelo e-mail (para evitar duplicação).
        """
        query = f"""
        query {{
          allCards(pipe_id: {pipe_id}, first: 50) {{
            edges {{
              node {{
                id
                title
                fields {{
                  name
                  value
                }}
              }}
            }}
          }}
        }}
        """
        response = requests.post(self.BASE_URL, headers=self.headers, json={"query": query})
        data = response.json()

        cards = data.get("data", {}).get("allCards", {}).get("edges", [])
        for edge in cards:
            fields = edge["node"]["fields"]
            for f in fields:
                if f["name"].lower() == "e-mail" and f["value"] == email:
                    return edge["node"]
        return None