from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.file_reader import read_txt, read_pdf
from app.preprocess import preprocess_text
from app.ai import classify_email, generate_reply

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(
    request: Request,
    email_text: str = Form(default=""),
    file: UploadFile | None = None
):
    text = ""

    # PRIORIDADE 1: TEXTO COLADO
    if email_text.strip():
        text = email_text

    # PRIORIDADE 2: ARQUIVO
    elif file and file.filename:
        filename = file.filename.lower()

        if not (filename.endswith(".txt") or filename.endswith(".pdf")):
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Formato inválido. Envie apenas .txt ou .pdf"
                }
            )

        if filename.endswith(".txt"):
            text = read_txt(file)
        else:
            text = read_pdf(file)

        if not text.strip():
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "error": "Não foi possível extrair texto do arquivo enviado."
                }
            )

    else:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Informe um texto ou envie um arquivo."
            }
        )

    clean_text = preprocess_text(text)
    category = classify_email(clean_text)
    reply = generate_reply(category)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "category": category,
            "reply": reply,
            "email_text": text
        }
    )
