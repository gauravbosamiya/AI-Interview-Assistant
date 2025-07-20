from fastapi import FastAPI, File, UploadFile, HTTPException
from api.api_utils import extract_text_from_file
from uuid import uuid4
import os
from pydantic import BaseModel, Field
from typing import Annotated, List
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from api.mongo import resume_collection

load_dotenv()

prompt = PromptTemplate(
    template="""
        I want you to act as an interviewer. Remember, you are the interviewer not the candidate. 

        Let’s think step by step.

        Based on the Resume, 
        Create a guideline with the following topics for an interview to test the knowledge of the candidate on necessary skills.
        
        The questions should be in the context of the resume.

        There are 4 main topics: 
        1. first question always ask to the candidate about yourself in briefly.
        2. Background and Skills 
        3. Work Experience
        4. Projects (if applicable)

        Generate only 10 relevant questions.
        Avoid repeating questions or phrasing.
        Even if the resume is the same, generate a **different set of questions** with **different structure, focus, or order**.

        Resume: 
        {context}

        Questions: {question}
    """, 
    input_variables=["context", "question"]
)

app = FastAPI()

class QuestionSchema(BaseModel):
    questions: Annotated[List[str], Field(..., description="Generated questions")]
    file_id: str
    filename: str


@app.get("/")
def home():
    return {"message": "AI Interview Assistant"}

@app.post("/generate-question", response_model=QuestionSchema)
async def generate_question(file: UploadFile = File(...)):
    allowed_types = ['.pdf', '.docx']
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in allowed_types:
        raise HTTPException(status_code=400, detail=f"Unsupported file type. Allowed types: {', '.join(allowed_types)}")

    content = await file.read()
    try:
        text = extract_text_from_file(content, file_extension)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {str(e)}")


    llm = ChatGroq(model="meta-llama/llama-4-maverick-17b-128e-instruct")
    formatted_prompt = prompt.format(context=text, question="")
    result = llm.invoke(formatted_prompt)

    lines = result.content.strip().split("\n")
    questions = [line.strip("-•1234567890. ").strip() for line in lines if "?" in line and line.strip().endswith("?")]
    questions = list(dict.fromkeys(questions))[:10]  

    file_id = str(uuid4())
    resume_collection.insert_one({
        "file_id": file_id,
        "filename": file.filename,
        "text": text,
        "questions":questions
    })
    
    return {"questions": questions, "file_id": file_id, "filename": file.filename}
