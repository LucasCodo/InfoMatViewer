from fastapi import APIRouter

from app import database
from app.auth import *
from app.response_models import *
from app.response_models import User
from typing import Annotated

router = APIRouter()


@router.post("/list-informational-material", response_model=InfoMatList)
async def create_list_info_mat(list_info_mat: InfoMatListPost,
                               user: Annotated[User, Depends(verify_google_token)]):
    """
        Endpoint para criar uma nova lista de materiais informativos.

        Args:
        - list_info_mat (InfoMatListPost): Representa os dados da nova lista de materiais
         informativos a ser criada.

        Returns:
        - InfoMatListPost: Retorna os dados da lista de materiais informativos criada.
    """
    return database.create_info_mat_list_and_add_items(user["email"], list_info_mat.name,
                                                       list_info_mat.public,
                                                       list(list_info_mat.listIDsInfoMats))


@router.get("/list-informational-material", response_model=list[InfoMatList])
async def get_my_lists(user: Annotated[User, Depends(verify_google_token)]):
    """
        Endpoint para obter as listas de materiais informativos de um usuário específico.

        Args:
        - user_email (EmailStr): O endereço de e-mail do usuário para recuperar suas listas de
         materiais informativos.

        Returns:
        - list[InfoMatList]: Uma lista de listas de materiais informativos associadas ao usuário.
    """
    return database.get_my_info_mat_lists(user["id"])


@router.post("/informational-material/review")
async def set_review(book_id: int, rating: float,
                     user: Annotated[User, Depends(verify_google_token)]):
    return database.add_or_update_review(user["id"], book_id, rating)


@router.delete("/informational-material/review")
async def delete_review(book_id: int,
                        user: Annotated[User, Depends(verify_google_token)]):
    return database.delete_review(book_id, user["id"])


@router.delete("/list-informational-material")
async def delete_list_informational_material(info_mat_list_id: int,
                                             user: Annotated[User, Depends(verify_google_token)]):
    return database.delete_info_mat_list(user["id"], info_mat_list_id)


@router.delete("/list-informational-material/item")
async def delete_item_in_list_informational_material(
        item_id: int, list_id: int,
        user: Annotated[User, Depends(verify_google_token)]):
    if (database.is_my_info_mat_list(user["id"], list_id) and
            database.info_mat_item_in_list(item_id, list_id)):
        return database.remove_info_mat_item_from_list(item_id, list_id)
    raise HTTPException(status_code=422)


@router.post("/list-informational-material/item")
async def add_item_in_list_informational_material(
        info_mat_id: int, info_mat_list_id: int,
        user: Annotated[User, Depends(verify_google_token)]):
    if database.is_my_info_mat_list(user["id"], info_mat_list_id):
        return database.add_info_mat_item_to_list(info_mat_id, info_mat_list_id)
    raise HTTPException(status_code=422)


@router.get("/permissions", response_model=list[Permission])
async def get_permissions(user: Annotated[User, Depends(verify_google_token)]):
    return user["permissions"]

'''
# Rota protegida que requer autenticação com um token do Google
@router.get("/me/", response_model=User)
async def protected_resource(user: User = Depends(verify_google_token)):
    # Você pode acessar as informações do usuário aqui
    return user
    '''
