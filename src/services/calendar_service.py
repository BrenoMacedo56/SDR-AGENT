from src.integrations.gcalendar import GoogleCalendarAPI


class CalendarService:
    def __init__(self):
        self.api = GoogleCalendarAPI()

    def get_slots(self, duration_minutes: int = 30, start_hour: int = 9, end_hour: int = 18, days: int = 7):
        """
        Retrieves available time slots from Google Calendar.

        :param duration_minutes: Duration of each meeting slot in minutes (default: 30)
        :param start_hour: Start of working hours (default: 9)
        :param end_hour: End of working hours (default: 18)
        :param days: Number of days ahead to check for availability (default: 7)
        :return: List of available slots as tuples (start_time_iso, end_time_iso)
        """
        return self.api.get_free_slots(
            duration_minutes=duration_minutes,
            start_hour=start_hour,
            end_hour=end_hour,
            days=days
        )

    def book_meeting(self, lead_name: str, lead_email: str, summary: str, description: str,
                     start_time: str, end_time: str):
        """
        Books a meeting in Google Calendar and automatically generates a Google Meet link.

        :param lead_name: Name of the person (lead)
        :param lead_email: Email of the person (lead)
        :param summary: Event title/summary
        :param description: Description or notes for the meeting
        :param start_time: Start time in RFC3339 format (e.g., '2025-10-31T14:00:00-03:00')
        :param end_time: End time in RFC3339 format (e.g., '2025-10-31T14:30:00-03:00')
        :return: Dictionary with event details (id, summary, meet_link, html_link, date)
        """
        return self.api.create_event(
            summary=summary,
            description=f"Lead: {lead_name} ({lead_email})\n\n{description}",
            start_time=start_time,
            end_time=end_time
        )