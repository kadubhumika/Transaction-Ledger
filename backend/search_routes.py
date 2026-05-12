from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.search_service import SearchService

router = APIRouter()

service = SearchService()


@router.get("/search/{query}")

def search_user(
    query: str,
    db: Session = Depends(get_db)
):

    return service.search_user(
        query,
        db
    )