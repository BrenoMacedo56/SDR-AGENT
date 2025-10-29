from src.integrations.gcalendar import CalComAPI

class CalendarService:
    def __init__(self):
        self.api = CalComAPI()

    def get_slots(self, username: str, event_type: str, start_date: str, end_date: str):
        """
        Obtém os próximos horários disponíveis.
        """
        return self.api.get_available_slots(username=username, event_type=event_type, start_date=start_date, end_date=end_date)

    def book_meeting(self, lead_name: str, lead_email: str, event_type: str, start_time: str):
        """
        Agenda uma reunião no Cal.com.
        """
        invitee = {
            "name": lead_name,
            "email": lead_email
        }
        booking = self.api.create_booking(event_type=event_type, invitee=invitee, start_time=start_time)
        return booking