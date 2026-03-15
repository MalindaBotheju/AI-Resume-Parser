from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
import fitz  # This is PyMuPDF

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResumeText(BaseModel):
    text: str

# We moved the AI logic into a helper function so both Text and PDF inputs can use it!
def call_ollama(text: str):
    # 1. We make the prompt much stricter
    prompt = f"""You are a strict data extraction tool. Extract the key information from the following resume.
You MUST respond with ONLY raw, valid JSON. Do not include any conversational text, introductions, markdown formatting, or notes.

### Resume Text:
{text}
"""
    payload = {
        "model": "hf.co/MalinZZZRayWed/Llama-3-Resume-Parser-GGUF",
        "prompt": prompt,
        "stream": False,
        "format": "json", # 2. THIS IS THE MAGIC KEY! It forces Ollama to only output JSON.
        "options": {
            "temperature": 0.0 # 3. Drop to 0.0 so it doesn't get creative
        }
    }
    
    response = requests.post("http://localhost:11434/api/generate", json=payload)
    response.raise_for_status()
    
    ai_response = response.json().get("response", "")
    
    try:
        clean_json = json.loads(ai_response)
        return {"status": "success", "data": clean_json}
    except:
        return {"status": "partial_success", "data": ai_response}

# Endpoint 1: For manual text pasting
@app.post("/api/extract")
def extract_data_text(resume: ResumeText):
    try:
        return call_ollama(resume.text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 2: NEW! For PDF file uploads
@app.post("/api/extract-pdf")
async def extract_data_pdf(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    try:
        # 1. Read the uploaded PDF file directly from memory
        pdf_bytes = await file.read()
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        # 2. Extract all the text from every page
        extracted_text = ""
        for page in doc:
            extracted_text += page.get_text()
            
        if not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text. Is this an image-based PDF?")
            
        # 3. Send the hidden text to our AI
        return call_ollama(extracted_text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi.responses import HTMLResponse
import os

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    # Read the index.html file and send it to the browser
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()