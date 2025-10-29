from src.services.calendar_service import CalendarService

class MeetingBookingWorkflow:
    def __init__(self, lead_repo, pipefy_service, response_generator):
        self.lead_repo = lead_repo
        self.pipefy_service = pipefy_service
        self.response_generator = response_generator
        self.calendar_service = CalendarService()  # 👈 Novo

    async def run(self, session_id: str, message: str, context: list[dict]):
        lead = self.lead_repo.get_lead(session_id)

        if lead and lead.get("status") == "qualificado":
            if "agendamento" not in lead:
                slots = self.calendar_service.get_slots("seu_usuario_calcom", "reuniao-consultoria")
                return await self.response_generator.generate(
                    context,
                    system_prompt=f"Ofereça um dos seguintes horários disponíveis: {slots}"
                )

            else:
                booking = self.calendar_service.book_meeting(
                    lead_name=lead["name"],
                    lead_email=lead["email"],
                    event_type="reuniao-consultoria",
                    start_time=lead["agendamento"]
                )

                # Atualiza Pipefy com link
                meeting_link = booking.get("booking", {}).get("url")
                self.pipefy_service.update_lead_card(
                    lead["pipefy_card_id"],
                    {"meeting_link": meeting_link}
                )

                self.lead_repo.update_status(session_id, "reunião_agendada")

                return await self.response_generator.generate(
                    context,
                    system_prompt=f"Reunião confirmada! Link: {meeting_link}. Agradeça o usuário."
                )

        else:
            return await self.response_generator.generate(
                context,
                system_prompt="Explique que precisamos qualificar antes de agendar uma reunião."
            )
