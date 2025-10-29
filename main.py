from fastapi import FastAPI
from API.routes import router as rest_router
from API.websocket import router as ws_router

app = FastAPI(title="Conversational SDR API")


app.include_router(rest_router, prefix="/api")
app.include_router(ws_router)

@app.get("/")
def root():
    return {"message": "✅ API do SDR funcionando!"}