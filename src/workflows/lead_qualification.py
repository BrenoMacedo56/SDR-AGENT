class LeadQualificationWorkflow:
    def __init__(self, lead_repo, response_generator):
        self.lead_repo = lead_repo
        self.response_generator = response_generator

    async def run(self, session_id: str, message: str, context: list[dict]):
        """
        Processa o estado   atual da qualificação e decide o próximo passo.
        """
        lead_data = self.lead_repo.get_lead(session_id)

        if not lead_data or "nome" not in lead_data:
            return await self.response_generator.generate(
                context,
                system_prompt="Politely ask for the lead's name to start the conversation."
            )

        if "email" not in lead_data:
            return await self.response_generator.generate(
                context,
                system_prompt="Now ask for their contact email, mentioning it will be used to send more details."
            )

        if "interesse" not in lead_data:
            return await self.response_generator.generate(
                context,
                system_prompt="Ask what their main challenge or interest is regarding the product."
            )

        self.lead_repo.update_status(session_id, "qualificado")
        return await self.response_generator.generate(
            context,
            system_prompt="Thank them for the information and say they seem ready for a meeting."
        )