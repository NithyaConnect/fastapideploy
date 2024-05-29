from fastapi import FastAPI, File, UploadFile, HTTPException
from typing import List
import fitz  # PyMuPDF

app = FastAPI()

def extract_text_from_pdf(pdf_file) -> List[str]:
    text_chunks = []
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    for page in doc:
        text = page.get_text()
        text_chunks.append(text)
    return text_chunks

@app.post("/upload/")
async def upload_pdf_and_extract_text(pdf_file: UploadFile = File(...)):
    if not pdf_file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Uploaded file is not a PDF.")
    
    try:
        text_chunks = extract_text_from_pdf(pdf_file.file)
        return {"text_chunks": text_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    #curl -X POST -F "pdf_file=@/path/to/your/file.pdf" http://localhost:8000/upload/

