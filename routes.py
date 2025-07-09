import io
import traceback
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from scripts.processor import process_pdf
from starlette.concurrency import run_in_threadpool

pdf_routes = APIRouter()

# Pydantic model for request body
class PDFUploadRequest(BaseModel):
    pdf_file: str  # URL
    password: str = ""

# Test Route
@pdf_routes.get("/test")
def test():
    return {"status": "ok"}

@pdf_routes.post("/upload-pdf")
async def upload_pdf(payload: PDFUploadRequest):
    print("Pdf Received, Request started...")
    try:
        pdf_url = payload.pdf_file
        password = payload.password

        if not pdf_url:
            raise HTTPException(status_code=400, detail="No PDF URL provided")

        response = requests.get(pdf_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to download PDF file")

        file_stream = io.BytesIO(response.content)

        print("PDF converted to bytes and moved to processing successfully...")
        # Process the PDF
        result_json = await run_in_threadpool(process_pdf, file_stream)

        return result_json

    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
