from firebase_admin import firestore
from datetime import datetime


class MeetingRepository:
    """
    Repositório responsável por gerenciar dados de reuniões (meetings) no Firestore.
    """

    def __init__(self):
        self.db = firestore.client()
        self.collection = self.db.collection("meetings")

    def create_meeting(self, session_id: str, meeting_data: dict) -> str:
        """
        Cria uma nova reunião no Firestore.
        Retorna o ID do documento criado.
        """
        meeting_data.update({
            "session_id": session_id,
            "created_at": datetime.utcnow()
        })

        doc_ref = self.collection.add(meeting_data)
        return doc_ref[1].id

    def update_meeting(self, meeting_id: str, updates: dict) -> None:
        """
        Atualiza uma reunião existente com novos dados.
        """
        self.collection.document(meeting_id).update(updates)

    def get_meeting(self, meeting_id: str) -> dict | None:
        """
        Retorna os dados de uma reunião pelo ID.
        """
        doc = self.collection.document(meeting_id).get()
        if doc.exists:
            return doc.to_dict()
        return None


    def list_meetings_by_session(self, session_id: str) -> list[dict]:
        """
        Lista todas as reuniões associadas a um session_id (usuário específico).
        """
        meetings = (
            self.collection
            .where("session_id", "==", session_id)
            .order_by("created_at", direction=firestore.Query.DESCENDING)
            .stream()
        )
        return [m.to_dict() for m in meetings]