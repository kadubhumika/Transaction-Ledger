from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from backend.database import get_db

from backend.profile_service import ProfileService

from backend.profile_data import (
    UpdateProfileData,
    AddBalanceData
)

router = APIRouter()

service = ProfileService()


@router.get("/profile/{email}")

def get_profile(
    email: str,
    db: Session = Depends(get_db)
):

    return service.get_profile(
        email,
        db
    )


@router.put("/profile/{email}")

def update_profile(
    email: str,
    data: UpdateProfileData,
    db: Session = Depends(get_db)
):

    return service.update_profile(
        email,
        data,
        db
    )


@router.post("/add-balance")

def add_balance(
    data: AddBalanceData,
    db: Session = Depends(get_db)
):

    return service.add_balance(
        data.email,
        data.amount,
        db
    )