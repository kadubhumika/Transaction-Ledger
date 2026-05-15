from fastapi import APIRouter

from backend.data_class import ScheduledPaymentCreate

from backend.scheduled_service import create_scheduled_payment

router = APIRouter()

@router.post("/schedule-payment")

async def schedule_payment(
    data: ScheduledPaymentCreate
):

    return create_scheduled_payment(data)