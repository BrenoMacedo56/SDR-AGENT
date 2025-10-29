from src.models.convsersation import Conversation
from src.DB.repositories.conversation_rep import ConversationRepository
from src.config.settings import Settings
#from src.utils.logger import get_logger

class ConversationManager:
    """
    Gerencia o contexto (histórico) das conversas dos usuários.
    No futuro, pode salvar em banco de dados ou cache.
    """

    def __init__(self):
        self.repo = ConversationRepository()

    def get_conversation(self, session_id: str):
        """
        Retorna o histórico da conversa de um usuário.
        """
        return self.repo.get_conversation(session_id)

    def update_conversation(self, session_id: str, role: str, content: str):
        """
        Atualiza o histórico da conversa (adiciona nova mensagem).
        """
        self.repo.save_message(session_id,role,content)