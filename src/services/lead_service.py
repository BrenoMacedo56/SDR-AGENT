from typing import Optional, Dict, Any, List
from datetime import datetime, timezone

from src.DB.repositories.lead_rep import LeadRepository


class LeadService:
    """
    Serviço responsável por gerenciar a lógica de leads.
    """

    def __init__(self):
        self.repository = LeadRepository()

    async def create_lead(self, name: str, email: str, phone: str, source: str = "chatbot") -> str:
        """
        Cria um novo lead.
        """
        print(f"Criando novo lead: {name} ({email})")
        lead_data = {
            "name": name,
            "email": email,
            "phone": phone,
            "source": source,
            "status": "new",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        return await self.repository.create_lead(lead_data)

    async def get_lead(self, lead_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca um lead pelo ID.
        """
        return await self.repository.get_lead(lead_id)

    async def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Busca um lead pelo e-mail.
        """
        return await self.repository.find_by_email(email)

    async def update_lead_status(self, lead_id: str, status: str):
        """
        Atualiza o status do lead (ex: 'new', 'qualified', 'meeting_scheduled', etc.).
        """
        update_data = {
            "status": status,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        await self.repository.update_lead(lead_id, update_data)

    async def update_lead_info(self, lead_id: str, updates: Dict[str, Any]):
        """
        Atualiza informações gerais do lead (ex: nome, telefone, email, etc.).
        """
        updates["updated_at"] = datetime.now(timezone.utc).isoformat(),
        await self.repository.update_lead(lead_id, updates)

    async def list_recent_leads(self, limit: int = 20) -> List[Dict[str, Any]]:
        """
        Lista os leads mais recentes.
        """
        return await self.repository.list_leads(limit)

    async def mark_as_contacted(self, lead_id: str):
        """
        Marca o lead como contatado.
        """
        await self.update_lead_status(lead_id, "contacted")

    async def mark_as_qualified(self, lead_id: str):
        """
        Marca o lead como qualificado.
        """
        await self.update_lead_status(lead_id, "qualified")

    async def mark_as_disqualified(self, lead_id: str):
        """
        Marca o lead como desqualificado.
        """
        await self.update_lead_status(lead_id, "disqualified")