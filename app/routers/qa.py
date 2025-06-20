from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.utils.file_parser import extract_text_from_pdf, extract_text_from_txt
from app.services.qa_engine import process_and_store, answer_question

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        ext = file.filename.split(".")[-1].lower()
        if ext == "pdf":
            text = extract_text_from_pdf(file.file)
        elif ext == "txt":
            text = extract_text_from_txt(file.file)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        process_and_store(text, namespace="user123")  # You can make namespace dynamic later
        return {"message": "File uploaded and processed successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")

@router.post("/ask")
async def ask_question(question: str = Form(...)):
    try:
        answer = answer_question(question, namespace="user123")
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")