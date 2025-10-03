from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from .detect import detect_type

app = FastAPI(title="Document Type Detector", version="0.1.0")

templates = Jinja2Templates(directory=str(Path(__file__).parent / 'templates'))

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/detect")
async def api_detect(file: UploadFile = File(...)):
    data = await file.read()
    doc_type, method = detect_type(file.filename, data)
    return {"filename": file.filename, "detected_type": doc_type, "method": method}

@app.post("/detect", response_class=HTMLResponse)
async def form_detect(request: Request, file: UploadFile = File(...)):
    data = await file.read()
    doc_type, method = detect_type(file.filename, data)
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "result": {
                "filename": file.filename,
                "detected_type": doc_type,
                "method": method
            }
        }
    )

# Simple health endpoint
@app.get("/healthz")
async def healthz():
    return JSONResponse({"status": "ok"})
