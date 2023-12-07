from fastapi import APIRouter

from app import database
from app.auth import *
from app.response_models import *
from app.response_models import User

router = APIRouter()


@router.post("/list-informational-material", response_model=InfoMatList)
async def create_list_info_mat(list_info_mat: InfoMatListPost,
                               user: User = Depends(verify_google_token)):
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
                                                       list_info_mat.listIDsInfoMats)


@router.get("/list-informational-material", response_model=list[InfoMatList])
async def get_my_lists(user: User = Depends(verify_google_token)):
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
                     user: User = Depends(verify_google_token)):
    return database.add_or_update_review(user["id"], book_id, rating)


@router.delete("/informational-material/review")
async def delete_review(book_id: int,
                        user: User = Depends(verify_google_token)):
    return database.delete_review(book_id, user["id"])


@router.delete("/list-informational-material")
async def delete_list_informational_material(info_mat_list_id: int,
                                             user: User = Depends(verify_google_token)):
    return database.delete_info_mat_list(info_mat_list_id)


@router.delete("/list-informational-material/item")
async def delete_item_list_informational_material(info_mat_id: int, info_mat_list_id: int,
                                                  user: User = Depends(verify_google_token)):
    return database.remove_info_mat_item_from_list(info_mat_id, info_mat_list_id)


@router.post("/list-informational-material/item")
async def add_item_list_informational_material(info_mat_id: int, info_mat_list_id: int,
                                               user: User = Depends(verify_google_token)):
    return database.add_info_mat_item_to_list(info_mat_id, info_mat_list_id)

'''
# Rota protegida que requer autenticação com um token do Google
@router.get("/me/", response_model=User)
async def protected_resource(user: User = Depends(verify_google_token)):
    # Você pode acessar as informações do usuário aqui
    return user
    '''
