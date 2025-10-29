from src.integrations.OpenAi_client import OpenAiClient
from src.prompts.system_p import intent_classifier
from src.utils.logger import Logger


logger = Logger()

class IntentClassifier:
    """
    Usa a API da OpenAI para classificar a intenção da mensagem do usuário.
    Exemplo: agendar, qualificar, encerrar, saudação etc.
    """
    def __init__(self):
        self.client = OpenAiClient()

    def classify(self, message: str) -> str:
        """
        Retorna a intenção provável da mensagem.
        """
        try:
            system_prompt = intent_classifier()

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ]

            response = self.client.send_message(messages)
            return response.strip().lower()

        except Exception as ex:
            return logger.error(f"Erro ao classificar intenção: {ex}")

