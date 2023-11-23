from app import database
from app.response_models import *
from fastapi import APIRouter
from pydantic import EmailStr

router = APIRouter()


@router.post("/list-informational-material", response_model=InfoMatList)
async def create_list_info_mat(user_email: EmailStr, list_info_mat: InfoMatListPost):
    """
        Endpoint para criar uma nova lista de materiais informativos.

        Args:
        - list_info_mat (InfoMatListPost): Representa os dados da nova lista de materiais
         informativos a ser criada.

        Returns:
        - InfoMatListPost: Retorna os dados da lista de materiais informativos criada.
    """
    return database.create_info_mat_list_and_add_items(user_email, list_info_mat.name,
                                                       list_info_mat.public,
                                                       list_info_mat.listIDsInfoMats)


@router.get("/list-informational-material/user/{user_email}", response_model=list[InfoMatList])
async def get_my_lists(user_email: EmailStr):
    """
        Endpoint para obter as listas de materiais informativos de um usuário específico.

        Args:
        - user_email (EmailStr): O endereço de e-mail do usuário para recuperar suas listas de
         materiais informativos.

        Returns:
        - list[InfoMatList]: Uma lista de listas de materiais informativos associadas ao usuário.
    """
    return database.get_my_info_mat_lists(database.read_user(user_email))


@router.post("/informational-material/review")
async def set_review(user_id: int, book_id: int, rating: float):
    return database.add_or_update_review(user_id, book_id, rating)


@router.delete("/informational-material/review")
async def delete_review(user_id: int, book_id: int):
    return database.delete_review(book_id, user_id)


@router.delete("/list-informational-material")
async def delete_list_informational_material(info_mat_list_id: int):
    return database.delete_info_mat_list(info_mat_list_id)


@router.delete("/list-informational-material/item")
async def delete_item_list_informational_material(info_mat_id: int, info_mat_list_id: int):
    return database.remove_info_mat_item_from_list(info_mat_id, info_mat_list_id)


@router.post("/list-informational-material/item")
async def add_item_list_informational_material(info_mat_id: int, info_mat_list_id: int):
    return database.add_info_mat_item_to_list(info_mat_id, info_mat_list_id)


@router.put("/informational-material")
async def add_item_list_informational_material(_info_mat: InfoMatUpdateModel):
    info_mat_id = _info_mat.id
    return database.update_info_mat(info_mat_id, **_info_mat.attrs)