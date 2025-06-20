import pdfplumber
from fastapi import APIRouter, UploadFile, File
from app.services.llm_summary import summarize_text

router = APIRouter()

@router.post("/upload")
async def summarize_file(file: UploadFile = File(...)):
    try:
        if file.filename.endswith(".pdf"):
            with pdfplumber.open(file.file) as pdf:
                all_text = ""
                for page in pdf.pages:
                    all_text += page.extract_text() or ""
            summary = summarize_text(all_text)
        else:
            content = await file.read()
            decoded = content.decode("utf-8", errors="ignore")
            summary = summarize_text(decoded)

        return {"summary": summary}

    except Exception as e:
        return {"error": str(e)}