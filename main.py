# main.py
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine
from backend.websocket_manager import manager

# Import routers safely
from backend.routes import auth_router
from backend.transaction_routes import router as txn_router
from backend.search_routes import router as search_router
from backend.profile_routes import router as profile_router
from backend.analytics_routes import router as analytics_router
from backend.pdf_routes import router as pdf_router
from backend.scheduled_routes import router as scheduled_router

from backend.scheduler_engine import start_scheduler

# Initialize FastAPI App
app = FastAPI()
app.include_router(scheduled_router)

# Move tables creation inside startup event to prevent premature process termination
@app.on_event("startup")
async def on_startup():
    print("Binding SQLAlchemy engine to PostgreSQL...")
    Base.metadata.create_all(bind=engine)
    print("Database tables validated successfully! ")
    await start_scheduler()
    print("Scheduler started successfully! ")

# Global Standard CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint Routing
app.include_router(auth_router)
app.include_router(txn_router)
app.include_router(search_router)
app.include_router(profile_router)
app.include_router(analytics_router)
app.include_router(pdf_router)

# WebSocket Endpoint Handler
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
