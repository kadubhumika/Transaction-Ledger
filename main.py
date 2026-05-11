from fastapi import FastAPI
from fastapi import WebSocket

from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine
from backend.routes import router
from backend.websocket_manager import manager


# create postgres tables

Base.metadata.create_all(bind=engine)


# fastapi app

app = FastAPI()


# cors

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# api routes

app.include_router(router)


# websocket route

@app.websocket("/ws/{email}")

async def websocket_endpoint(
    websocket: WebSocket,
    email: str
):

    await manager.connect(email, websocket)

    try:

        while True:

            await websocket.receive_text()

    except:

        manager.disconnect(email)