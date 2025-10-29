from google.cloud import firestore
from datetime import datetime

class LogRepository:
    def __init__(self):
        self.db = firestore.Client()
        self.collection = self.db.collection("logs")

    def log_event(self, session_id: str, event_type: str, details: dict):
        data = {
            "session_id": session_id,
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.utcnow()
        }
        try:
            self.collection.add(data)
        except Exception as e:
            print(f"[LOG ERROR] Failed to log event: {e}")