from datetime import datetime, timezone
from typing import Dict, Any
from src.integrations.pipefy import pipefyClient
from src.config.settings import Settings


class PipefyService:
    def __init__(self):
        self.pipefy_api = pipefyClient()
        self.pipe_id = Settings.PIPE_ID

    def _build_card_fields(self, lead_data: Dict[str, Any]) -> list[dict]:
        """
        Constrói os campos no formato aceito pela Pipefy API.
        """
        return [
            {"field_id": "nome", "field_value": lead_data.get("nome")},
            {"field_id": "e_mail", "field_value": lead_data.get("email")},
            {"field_id": "empresa", "field_value": lead_data.get("Empresa")},
            {"field_id": "interesse", "field_value": lead_data.get("interest", "Não especificado")},
            {"field_id": "status", "field_value": lead_data.get("status", "Novo")},
            {"field_id": "necessidade", "field_value": lead_data.get("Necessidade")},
            {"field_id": "interesse_confirmado", "field_value": lead_data.get("interesse_confirmado")},
            {"field_id": "data_criacao", "field_value": datetime.now(timezone.utc).isoformat()}
        ]

    async def create_lead_card(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo card de lead no Pipefy.
        """
        fields = self._build_card_fields(lead_data)
        return await self.pipefy_api.create_card(self.pipe_id, fields)

    async def update_lead_card(self, card_id: str, update_data: dict) -> Dict[str, Any]:
        """
        Atualiza um card existente no Pipefy.
        """
        fields = [{"field_id": k, "field_value": v} for k, v in update_data.items()]
        return await self.pipefy_api.update_card(card_id, fields)