import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from file_reader import read_pdf, read_txt
from classifier import classify_email, generate_reply, summarize_email

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyze")
async def analyze(
    email_text: str = Form(default=""),
    file: UploadFile | None = None
):
    text = ""

    if file and file.filename:
        filename = file.filename.lower()

        if filename.endswith(".txt"):
            text = read_txt(file)  

        elif filename.endswith(".pdf"):
            text = read_pdf(file)  

        else:
            return JSONResponse(
                status_code=400,
                content={"error": "Formato de arquivo não suportado. Use .txt ou .pdf"}
            )

    else:
        text = email_text.strip()

    if not text:
        return JSONResponse(
            status_code=400,
            content={"error": "O email não pode estar vazio"}
        )

    print(f"[DEBUG] Texto recebido ({len(text)} chars): {text[:200]}...")
    
    if len(text.strip()) < 20:
        return JSONResponse(
            status_code=400,
            content={"error": "O email é muito curto para análise"}
        )

    category = classify_email(text)
    response = generate_reply(category, text)  
    summary = summarize_email(text)

    return {
        "category": category,
        "summary": summary,
        "response": response
    }