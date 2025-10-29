import os
from venv import logger

from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '..', '.env')
load_dotenv(ENV_PATH)

##from src.utils.logger import get_logger
##from src.config.settings import settings

##logger = get_logger(__name__)

class OpenAiClient:
    """
        Classe responsável por gerenciar a comunicação com a API da OpenAI.
        Ela abstrai a complexidade da integração, permitindo que o restante
        do sistema apenas chame 'send_message' sem se preocupar com autenticação,
        formatação ou tratamento de erros.
    """

    def __init__(self):
        try:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("API key not found")

            self.client = OpenAI(api_key=api_key)
            self.default_model = "gpt-4.1"

        except Exception as ex:
            logger.error(f"Error during OpenAI API inicialization {str(ex)}")
            raise

    def send_message(self,
                     messages: List[Dict[str, str]],
                     model: Optional[str] = None,
                     temperature: float = 0.7,
                     max_tokens: int = 500):
        try:
            model_name = model or self.default_model

            response = self.client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            content = response.choices[0].message.content.strip()
            return content

        except Exception as e:
            logger.error(f"Erro ao comunicar com a OpenAI: {str(e)}")
            raise

    def stream_response(self, messages: List[Dict[str, str]]):
        """
        Retorna a resposta em tempo real (streaming) — ideal para WebSocket.
        """
        for chunk in self.client.chat.completions.create(
                model=self.default_model,
                messages=messages,
                stream=True,
        ):
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
