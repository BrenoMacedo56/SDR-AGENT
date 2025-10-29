import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    PIPEFY_API_KEY: str = os.getenv("PIPEFY_API_KEY", "")
    CALENDLY_API_KEY: str = os.getenv("CALENDLY_API_KEY", "")
    CAL_COM_API_KEY: str = os.getenv("CAL_COM_API_KEY", "")
    GOOGLE_SERVICE_ACCOUNT_FILE: str = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "")
    GOOGLE_CALENDAR_ID: str = os.getenv("GOOGLE_CALENDAR_ID", "")
    PIPE_ID: str = os.getenv("PIPE_ID", "")
    GOOGLE_APPLICATION_CREDENTIALS: str = "FIREBASE.json"


    def validation(self):
        """
        basics validations
        """
        if not self.OPENAI_API_KEY:
            raise ValueError("OPEN AI Key not found")

        if not self.PIPEFY_API_KEY:
            raise ValueError("PIPEFY Key not found")

        if not self.CALENDLY_API_KEY:
            raise ValueError("CALENDLY Key not found")

        return True