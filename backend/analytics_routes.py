from fastapi import APIRouter
from backend.analytics_service import get_user_analytics

router = APIRouter()

@router.get("/analytics/{email}")
def analytics(email: str):

    return get_user_analytics(email)