import asyncio
from concurrent.futures import ThreadPoolExecutor
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine
from backend.websocket_manager import manager
from backend.bank_account_routes import router as bank_router
from dotenv import load_dotenv

load_dotenv()

from backend.routes import auth_router
from backend.transaction_routes import router as txn_router
from backend.search_routes import router as search_router
from backend.profile_routes import router as profile_router
from backend.analytics_routes import router as analytics_router
from backend.pdf_routes import router as pdf_router
from backend.scheduled_routes import router as scheduled_router
from backend.scheduler_engine import start_scheduler

app = FastAPI()

def init_db():
    print("Binding SQLAlchemy engine to PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("Database tables validated successfully! ")

@app.on_event("startup")
async def on_startup():
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, init_db)
    await start_scheduler()
    print("🔥 Scheduler started!")
    print("Scheduler started successfully! ")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(scheduled_router)
app.include_router(txn_router)
app.include_router(search_router)
app.include_router(profile_router)
app.include_router(analytics_router)
app.include_router(pdf_router)
app.include_router(bank_router)

@app.websocket("/ws/{email}")
async def websocket_endpoint(websocket: WebSocket, email: str):
    print(f"Incoming connection handshake from: {email}")
    await manager.connect(email, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(f"WS Msg from {email}: {data}")
    except Exception as e:
        print(f"WS Loop Exception for {email}: {e}")
    finally:
        manager.disconnect(email)
