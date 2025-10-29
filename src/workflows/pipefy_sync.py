from src.services.pipefy_service import PipefyService

class PipefySyncWorkflow:
    def __init__(self):
        self.pipefy_service = PipefyService()

    async def sync_after_qualification(self, lead_data: dict):
        """
        Cria ou atualiza um card no Pipefy após o lead ser qualificado.
        """
        card = await self.pipefy_service.create_lead_card(lead_data)
        return card

    async def update_after_meeting(self, card_id: str, meeting_data: dict):
        """
        Atualiza card no Pipefy com dados da reunião agendada.
        """
        card = await self.pipefy_service.update_lead_card(card_id, meeting_data)
        return card