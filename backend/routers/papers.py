from fastapi import UploadFile, APIRouter, HTTPException
from services import ai, pdf

router = APIRouter(
    prefix="/papers",
    tags=["papers"],
)

@router.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid content type. Only PDF files are allowed.")
    
    contents = await file.read()
    text = pdf.extract_text(contents)
    summary = ai.summarize_text(text)
    return {"filename": file.filename, "summary": summary}

