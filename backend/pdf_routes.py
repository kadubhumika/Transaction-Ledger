from fastapi import APIRouter
from fastapi.responses import FileResponse

from backend.pdf_service import generate_pdf_statement

router = APIRouter()

@router.get("/download-statement/{email}")

async def download_statement(email: str):

    filename = generate_pdf_statement(email)

    return FileResponse(
        path=filename,
        media_type='application/pdf',
        filename=filename
    )