from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import EmailStr

import database
from configs import AppSettings
from response_models import *

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request,
                                                     "admin_email": AppSettings().admin_email})


@app.get("/informational-material/{info_mat_id}", response_model=InfoMatBasic)
async def info_mat(info_mat_id: int):
    return database.read_info_mat_basic(info_mat_id)


@app.get("/informational-material/{info_mat_id}/details", response_model=InfoMat)
async def info_mat_details(info_mat_id: int):
    return database.read_info_mat(info_mat_id)


@app.get("/search/informational-material/", response_model=list[InfoMat])
async def search_info_mat(value: str):
    return database.search_info_mat(value)


@app.get("/list-informational-material/{cod}")
async def get_public_list_informational_material(cod: int):
    print(cod)
    return {}


@app.post("/informational-material/")
async def add_info_mat(new_info_mat: InfoMat):
    return database.create_info_mat(**dict(new_info_mat))


@app.post("/list-informational-material")
async def create_list_info_mat(list_info_mat: InfoMatList):
    return list_info_mat


@app.get("/list-informational-material/user/{user_email}", response_model=list[InfoMatList])
async def get_my_lists(user_email: EmailStr):
    return database.get_my_info_mat_lists(database.read_user(user_email))
