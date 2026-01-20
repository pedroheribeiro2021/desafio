from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.ai import classify_email, generate_reply
from app.preprocess import preprocess_text

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze", response_class=HTMLResponse)
async def analyze(request: Request, email_text: str = Form(...)):
    clean_text = preprocess_text(email_text)
    category = classify_email(clean_text)
    reply = generate_reply(email_text, category)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "category": category,
            "reply": reply,
            "email_text": email_text
        }
    )
