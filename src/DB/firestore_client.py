import os
import firebase_admin
from firebase_admin import credentials, firestore
from src.config.settings import Settings

class FirestoreClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)


            cred_path = Settings.GOOGLE_APPLICATION_CREDENTIALS
            if not cred_path:
                raise ValueError("Caminho da credencial do Firestore não configurado.")

            if not firebase_admin._apps:
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)

            cls._instance.db = firestore.client()
        return cls._instance