from datetime import datetime
from typing import Dict, Any
from zoneinfo import ZoneInfo

from src.integrations.pipefy import pipefyClient
import os
from src.config.settings import Settings


class PipefyService:
    def __init__(self):
        self.pipefy_api = pipefyClient()
        self.pipe_id = Settings.PIPE_ID

    def _build_card_payload(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Constrói o payload GraphQL no formato aceito pela Pipefy API.
        """
        name = lead_data.get("nome")
        email = lead_data.get("E-mail")
        empresa = lead_data.get("Empresa")
        necessidade = lead_data.get("Necessidade")
        interest = lead_data.get("interest", "Não especificado")
        interest_confirm = lead_data.get("interesse_confirmado", "Não identificado")
        status = lead_data.get("status", "Novo")
        created_at = datetime.now(ZoneInfo("America/Sao_Paulo")).isoformat(),
        meeting_link = lead_data.get("link_da_reuniao"),
        meeting_datetime = lead_data.get("data_da_reuniao")

        return {
            "title": f"Lead: {name or 'Sem nome'}",
            "fields_attributes": [
                {"field_id": "nome", "field_value": name},
                {"field_id": "e_mail", "field_value": email},
                {"field_id": "empresa", "field_value": empresa},
                {"field_id": "interesse", "field_value": interest},
                {"field_id": "interesse_confirmado", "field_value": interest_confirm},
                {"field_id": "status", "field_value": status},
                {"field_id": "necessidade", "field_value": necessidade},
                {"field_id": "data_criacao", "field_value": created_at},
                {"field_id": "link_da_reuniao", "field_value": meeting_link},
                {"field_id": "data_da_reuniao", "field_value": meeting_datetime}
            ],
        }
    async def create_lead_card(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo card de lead no Pipefy.
        """
        payload = self._build_card_payload(lead_data)
        pipe_id = self.pipe_id
        return await self.pipefy_api.create_card(pipe_id, payload)


    def update_lead_card(self, card_id: str, update_data: dict):
        fields = [{"field_id": key, "field_value": value} for key, value in update_data.items()]
        return self.pipefy_api.update_card(card_id, fields)