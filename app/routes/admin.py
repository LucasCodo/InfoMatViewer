
from fastapi import APIRouter

from app import database
from app.auth import *
from app.response_models import *

router = APIRouter()


@router.post("/informational-material/")
async def add_info_mat(new_info_mat: InfoMat, user: User = Depends(verify_google_token)):
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
async def delete_informational_material(info_mat_id: int,
                                        user: User = Depends(verify_google_token)):
    return database.delete_info_mat(info_mat_id)


@router.put("/informational-material")
async def update_informational_material(_info_mat: InfoMatUpdateModel,
                                        user: User = Depends(verify_google_token)):
    info_mat_id = _info_mat.id
    return database.update_info_mat(info_mat_id, **_info_mat.attrs)


@router.get("/informational-material/all", response_model=list[InfoMat])
async def get_all_informational_material(user: User = Depends(verify_google_token)):
    return database.get_all_info_mat()
