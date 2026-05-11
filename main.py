# main.[y
#run app
from fastapi import FastAPI

from backend import *

from backend import *

from backend import *
from backend.database import Base, engine
from backend.routes import router
from fastapi import FastAPI, WebSocket
from backend.websocket_manager import manager

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router)
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