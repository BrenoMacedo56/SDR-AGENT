from fastapi import APIRouter
from src.agents.cv_agent import CVAgent

router = APIRouter()
agent = CVAgent()

@router.post("/chat")
async def chat(session_id: str, message: str):
    """
    Endpoint simples para enviar mensagens via REST.
    """
    response = agent.handler_user_msg(session_id, message)
    return {"session_id": session_id, "response": response}