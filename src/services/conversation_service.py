from typing import Optional, Dict, Any, List
from datetime import datetime

from src.DB.repositories.conversation_rep import ConversationRepository


class ConversationService:
    """
    Serviço responsável por gerenciar a lógica de conversas.
    """

    def __init__(self):
        self.repository = ConversationRepository()

    async def start_conversation(self, lead_id: str, first_message: str) -> str:
        """
        Inicia uma nova conversa para um lead.
        Se já houver uma conversa aberta, reutiliza-a.
        """
        existing_conversation = await self.repository.get_conversation_by_lead(lead_id)

        if existing_conversation:
            print(f"Conversa existente encontrada para o lead {lead_id}.")
            return existing_conversation["id"]

        print(f"Criando nova conversa para o lead {lead_id}.")
        return await self.repository.create_conversation(lead_id, first_message)

    async def add_message(self, conversation_id: str, sender: str, content: str):
        """
        Adiciona uma nova mensagem na conversa.
        """
        print(f"Adicionando mensagem à conversa {conversation_id} ({sender}): {content}")
        await self.repository.add_message(conversation_id, sender, content)

    async def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """
        Recupera uma conversa específica.
        """
        return await self.repository.get_conversation(conversation_id)

    async def get_active_conversation(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """
        Retorna a conversa ativa de um lead.
        """
        return await self.repository.get_conversation_by_lead(lead_id)

    async def close_conversation(self, conversation_id: str):
        """
        Encerra uma conversa (muda status para 'closed').
        """
        print(f"Encerrando conversa {conversation_id}.")
        await self.repository.close_conversation(conversation_id)

    async def list_recent_conversations(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Lista conversas recentes, ordenadas por atualização.
        """
        return await self.repository.list_conversations(limit)