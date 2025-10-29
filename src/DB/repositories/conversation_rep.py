from src.models.convsersation import Conversation
from src.DB.firestore_client import FirestoreClient
from google.cloud import firestore



class ConversationRepository:
    def __init__(self):
        self.db = FirestoreClient().db
        self.collection = self.db.collection("conversations")

    def save_message(self, session_id: str, role: str, content: str):
        """Salva uma mensagem no Firestore dentro da subcoleção messages"""
        conversation_ref = self.collection.document(session_id)
        conversation_ref.collection("messages").add({
            "role": role,
            "content": content,
            "timestamp": firestore.SERVER_TIMESTAMP
        })

    def get_conversation(self, session_id: str):
        """Recupera todas as mensagens da conversa"""
        conversation_ref = self.collection.document(session_id)
        docs = conversation_ref.collection("messages").order_by("timestamp").stream()
        return [doc.to_dict() for doc in docs]