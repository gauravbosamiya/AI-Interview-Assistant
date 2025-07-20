from fastapi import FastAPI, File, UploadFile, HTTPException
from api.api_utils import extract_text_from_file
from uuid import uuid4
import os

app = FastAPI()

@app.get("/")
def home():
    return {'message':'AI Interview Assistant'}

@app.post("/upload-resume")
async def upload_resume(file:UploadFile=File(...)):
    allowed_type=['.pdf','.docx']
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    if file_extension not in allowed_type:
        raise HTTPException(status_code=400, detail=f"Unsupported file type Allowed file types are : {', '.join(allowed_type)}")
    
    
    content = await file.read()
    
    try:
        text = extract_text_from_file(content, file_extension)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")

    return {"file_id":str(uuid4),"filename": file.filename, "text_snippet": text}
