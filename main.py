from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from configs import AppSettings
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "admin_email": AppSettings().admin_email})


@app.get("/informational-material")
async def info_mat():
    return {}


@app.get("/informational-material/details")
async def info_mat():
    return {}


@app.get("/list-informational-material/{cod}")
async def info_mat(cod: int):
    print(cod)
    return {}


@app.get("/list-informational-material")
async def info_mat():
    return {}


