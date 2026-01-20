from google.cloud import firestore
from datetime import datetime

class LeadRepository:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection("leads")

    def upsert_lead(self, session_id: str, data: dict):
        """
        Cria ou atualiza os dados de um lead baseado na sessão.
        """
        leads_query = self.collection.where("session_id", "==", session_id).limit(1).stream()
        lead_doc = next(leads_query, None)

        if lead_doc:
            self.collection.document(lead_doc.id).update({
                **data,
                "updated_at": datetime.utcnow()
            })
        else:
            self.collection.add({
                "session_id": session_id,
                **data,
                "created_at": datetime.utcnow(),
            })

    def get_lead(self, session_id: str):
        """
        Retorna o lead associado à sessão.
        """
        leads_query = self.collection.where("session_id", "==", session_id).limit(1).stream()
        lead_doc = next(leads_query, None)
        return lead_doc.to_dict() if lead_doc else None

    def update_status(self, session_id: str, new_status: str):
        """
        Atualiza o status do lead (ex: 'qualificado', 'agendado', 'finalizado').
        """
        leads_query = self.collection.where("session_id", "==", session_id).limit(1).stream()
        lead_doc = next(leads_query, None)

        if lead_doc:
            self.collection.document(lead_doc.id).update({
                "status": new_status,
                "updated_at": datetime.utcnow()
            })
            print(f"[LEAD] Status atualizado para '{new_status}' - sessão: {session_id}")
        else:
            print(f"[LEAD] Nenhum lead encontrado para sessão {session_id}")