from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.file_reader import read_pdf, read_txt
from app.classifier import classify_email, generate_reply, summarize_email

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

    # ✅ SÓ entra aqui se REALMENTE tiver arquivo
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
        # ✅ texto digitado
        text = email_text.strip()

    if not text:
        return JSONResponse(
            status_code=400,
            content={"error": "O email não pode estar vazio"}
        )

    category = classify_email(text)
    response = generate_reply(category)
    summary = summarize_email(text)

    return {
        "category": category,
        "summary": summary,
        "response": response
    }
