from fastapi import FastAPI
from fastapi import WebSocket

from fastapi.middleware.cors import CORSMiddleware

from backend.database import Base, engine

from backend.websocket_manager import manager
from backend.transaction_routes import router as txn_router
from backend.search_routes import router as search_router

from backend.profile_routes import router as profile_router
from backend.routes import auth_router


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

app.include_router(auth_router)

app.include_router(txn_router)
app.include_router(search_router)

app.include_router(profile_router)


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

