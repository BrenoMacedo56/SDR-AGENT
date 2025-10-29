from fastapi import WebSocket, WebSocketDisconnect, APIRouter
from src.agents.cv_agent import CVAgent

router = APIRouter()
agent = CVAgent()

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """
    Canal WebSocket — comunicação em tempo real com o agente.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            response = agent.handler_user_msg(session_id, data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print(f"Sessão {session_id} desconectada.")