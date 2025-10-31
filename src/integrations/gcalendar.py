import os
import datetime
import uuid
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from dotenv import load_dotenv
from src.config.settings import Settings

# Defina os escopos necessários
SCOPES = ["https://www.googleapis.com/auth/calendar"]


class GoogleCalendarAPI:
    def __init__(self):
        creds = None

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                # Tenta renovar o token automaticamente
                creds.refresh(Request())
            else:
                raise FileNotFoundError(
                    "O arquivo 'token.json' não foi encontrado ou está inválido. "
                    "Rode o script de autenticação (Passo 1) para gerar o token OAuth."
                )

        self.calendar_id = Settings.GOOGLE_CALENDAR_ID
        if not self.calendar_id:
            raise ValueError(
                "A variável GOOGLE_CALENDAR_ID deve estar configurada nas suas Settings."
            )

        self.service = build("calendar", "v3", credentials=creds)

    def create_event(self, summary, description, start_time, end_time):
        """
        Cria um evento no Google Calendar com link automático do Google Meet.
        """

        event = {
            "summary": summary,
            "description": description,
            "start": {"dateTime": start_time, "timeZone": "America/Sao_Paulo"},
            "end": {"dateTime": end_time, "timeZone": "America/Sao_Paulo"},
            "conferenceData": {
                "createRequest": {
                    "requestId": str(uuid.uuid4()),
                    "conferenceSolutionKey": {"type": "hangoutsMeet"}
                }
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "popup", "minutes": 10}
                ],
            },
        }
        event = self.service.events().insert(
            calendarId=self.calendar_id,
            body=event,
            conferenceDataVersion=1
        ).execute()

        # --- Lógica para formatação da data ---
        # 1. Extrair a string de data/hora de início do evento (formato RFC3339)
        start_datetime_str = event["start"]["dateTime"]

        # 2. Converter a string para um objeto datetime
        start_datetime_obj = datetime.datetime.fromisoformat(start_datetime_str)

        # 3. Formatar o objeto datetime para a string "DD/MM/YY"
        formatted_date = start_datetime_obj.strftime("%d/%m/%y")
        # --------------------------------------

        return {
            "id": event.get("id"),
            "summary": event.get("summary"),
            "meet_link": event["conferenceData"]["entryPoints"][0]["uri"],
            "html_link": event.get("htmlLink"),
            "date": formatted_date  # Agora retorna a data formatada como DD/MM/YY
        }

    def list_events(self, max_results=20):
        """
        Lista os próximos eventos do calendário.
        Aumentamos max_results para buscar mais eventos para o cálculo de slots.
        """
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()

        future_date = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
        time_max = future_date.isoformat()

        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=now,
            timeMax=time_max,  # Limita a busca aos próximos 7 dias
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()

        return events_result.get("items", [])

    def get_free_slots(self, duration_minutes=30, start_hour=9, end_hour=18, days=7):
        """
        Calcula e retorna slots de horários livres para agendamento.

        :param duration_minutes: Duração da reunião em minutos (ex: 30, 60).
        :param start_hour: Hora de início do horário de trabalho (ex: 9 para 09:00).
        :param end_hour: Hora de fim do horário de trabalho (ex: 18 para 18:00).
        :param days: Número de dias para buscar slots (ex: 7).
        :return: Lista de slots disponíveis como tuplas (start_time_iso, end_time_iso).
        """

        events = self.list_events(max_results=100)  # Aumentar o limite para garantir cobertura dos 7 dias

        occupied_slots = []
        for event in events:
            if 'dateTime' in event['start'] and 'dateTime' in event['end']:
                start = datetime.datetime.fromisoformat(event['start']['dateTime'])
                end = datetime.datetime.fromisoformat(event['end']['dateTime'])
                occupied_slots.append((start, end))

        now = datetime.datetime.now(datetime.timezone.utc)
        search_end_date = now + datetime.timedelta(days=days)

        free_slots = []
        current_date = now.date()

        tz = datetime.timezone(datetime.timedelta(hours=-3))  # UTC-3 para America/Sao_Paulo

        while current_date <= search_end_date.date():
            if current_date.weekday() >= 5:
                current_date += datetime.timedelta(days=1)
                continue

            day_start = datetime.datetime(
                current_date.year,
                current_date.month,
                current_date.day,
                start_hour,
                0,
                0,
                tzinfo=tz
                )
            day_end = datetime.datetime(
                current_date.year,
                current_date.month,
                current_date.day,
                end_hour,
                0,
                0,
                tzinfo=tz
                )

            current_slot_start = max(day_start, now.astimezone(tz))

            daily_occupied = sorted(
                [
                    (s.astimezone(tz), e.astimezone(tz)) for s, e in occupied_slots
                    if s.date() == current_date or e.date() == current_date
                ], key=lambda x: x[0]
            )

            daily_occupied.append((day_end, day_end))

            for occupied_start, occupied_end in daily_occupied:
                if current_slot_start + datetime.timedelta(minutes=duration_minutes) <= occupied_start:
                    free_start = current_slot_start
                    free_end = occupied_start

                    while free_start + datetime.timedelta(minutes=duration_minutes) <= free_end:
                        slot_end = free_start + datetime.timedelta(minutes=duration_minutes)

                        if slot_end <= day_end:
                            free_slots.append(
                                (
                                    free_start.astimezone(datetime.timezone.utc).isoformat(),
                                    slot_end.astimezone(datetime.timezone.utc).isoformat()
                                )
                            )

                        free_start = slot_end

                current_slot_start = max(current_slot_start, occupied_end)

            current_date += datetime.timedelta(days=1)

        return free_slots