from datetime import datetime

class Conversation:
    def __init__(self, session_id: str, role: str, content: str, created_at: datetime | None = None):
        self.session_id = session_id
        self.role = role
        self.content = content
        self.created_at = created_at or datetime.utcnow()