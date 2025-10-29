from http.client import responses
from src.DB.repositories.conversation_rep import ConversationRepository
from src.DB.repositories.lead_rep import LeadRepository
from src.DB.repositories.log_rep import LogRepository
from src.agents.intent_classifier import IntentClassifier
from src.integrations.OpenAi_client import OpenAiClient
from src.agents.cv_manager import ConversationManager
from src.workflows.lead_qualification import LeadQualificationWorkflow
from src.workflows.meet_booking import MeetingBookingWorkflow
from src.services.pipefy_service import pipefyClient
from src.models.convsersation import Conversation
from src.prompts.system_p import intent_classifier
from src.workflows.pipefy_sync import PipefySyncWorkflow


#from src.utils.logger import get_logger

class CVAgent:
    """
       Agente principal responsável por interagir com o usuário,
       gerenciar o contexto da conversa e gerar respostas usando a OpenAI.
    """

    def __init__(self):
        self.client = OpenAiClient()
        self.pipefy_client = pipefyClient()
        self.conversation_manager = ConversationManager()
        self.intent_classifier = IntentClassifier()
        self.conversation_repo = ConversationRepository()
        self.lead_repo = LeadRepository()
        self.log_repo = LogRepository()
        self.lead_qualification_workflow = LeadQualificationWorkflow(
            self.lead_repo, self.client
        )
        self.meeting_booking_workflow = MeetingBookingWorkflow(
            self.lead_repo, None, self.pipefy_client  # o segundo parâmetro pode ser o pipefy_service se já estiver pronto
        )
        self.pipefy_sync = PipefySyncWorkflow()

    def handler_user_msg(self, session_id: str, message: str) -> str:
        """
        Recebe uma mensagem do usuário, atualiza o contexto e retorna a resposta da IA.
        Integra os fluxos de qualificação e agendamento conforme o status do lead.
        """
        try:
            self.conversation_repo.save_message(session_id, "user", message)
            self.log_repo.log_event("mensagem_recebida", {"session_id": session_id, "conteudo": message})

            conversation_history = self.conversation_manager.get_conversation(session_id)
            conversation_history.append({"role": "user", "content": message})
            self.conversation_manager.update_conversation(session_id, "user", message)

            lead_data = self.lead_repo.get_lead(session_id)
            lead_status = lead_data.get("status") if lead_data else "novo"
            lead_data = self.lead_repo.get_lead(session_id)
            if lead_data and lead_data.get("status") == "Qualificado":
                self.pipefy_sync.sync_after_qualification(lead_data)
                self.log_repo.log_event("pipefy_sync", {"session_id": session_id, "lead": lead_data})

            if lead_status in ["novo", "em_qualificacao"]:
                response = self.lead_qualification_workflow.run(session_id, message, conversation_history)
                self.log_repo.log_event("fluxo", {"session_id": session_id, "etapa": "qualificação"})

            elif lead_status == "qualificado":
                response = self.meeting_booking_workflow.run(session_id, message, conversation_history)
                self.log_repo.log_event("fluxo", {"session_id": session_id, "etapa": "agendamento"})

            else:
                response = self.client.send_message(conversation_history)

            self.conversation_repo.save_message(session_id, "assistant", response)
            self.conversation_manager.update_conversation(session_id, "assistant", response)

            return response

        except Exception as e:
            self.log_repo.log_event("erro", {"session_id": session_id, "erro": str(e)})
            return "Desculpe, encontrei um erro ao processar sua mensagem."
