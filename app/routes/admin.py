
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr

from app import database
from app.response_models import *


router = APIRouter()


@router.post("/informational-material/")
async def add_info_mat(new_info_mat: InfoMat):
    """
        Endpoint para adicionar um novo materiais informacional.

        Args:
        - new_info_mat (InfoMat): Novo materiais informacional a ser adicionado.

        Returns:
        - None: Retorna nada ou uma confirmação de sucesso, dependendo da implementação do método
        `create_info_mat` no objeto `database`.
    """
    return database.create_info_mat(**dict(new_info_mat))


@router.delete("/informational-material")
async def delete_informational_material(info_mat_id: int):
    return database.delete_info_mat(info_mat_id)


@router.put("/informational-material")
async def update_informational_material(info_mat: InfoMat):
    return database.update_info_mat(**dict(info_mat))


@router.get("/informational-material/all")
async def get_all_informational_material():
    return database.get_all_info_mat()
