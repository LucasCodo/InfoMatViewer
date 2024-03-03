from fastapi import APIRouter

from app import database
from app.auth import *
from app.response_models import *
from app.enumerations import PermissionsType
from datetime import timedelta

router = APIRouter()


@router.post("/informational-material")
async def add_info_mat(new_info_mat: InfoMatPost, user: User = Depends(verify_google_token)):
    """
        Endpoint para adicionar um novo materiais informacional.

        Args:
        - new_info_mat (InfoMatPost): Novo materiais informacional a ser adicionado.

        Returns:
        - None: Retorna nada ou uma confirmação de sucesso, dependendo da implementação do método
        `create_info_mat` no objeto `database`.
    """
    for permission in user["permissions"]:
        if permission.permission_type in [PermissionsType.FULL.name,
                                          PermissionsType.CREATE_INFO_MAT.name]:
            return database.create_info_mat(**dict(new_info_mat))
    raise HTTPException(status_code=401)


@router.delete("/informational-material")
async def delete_informational_material(info_mat_id: int,
                                        user: User = Depends(verify_google_token)):
    for permission in user["permissions"]:
        if permission.permission_type in [PermissionsType.FULL.name,
                                          PermissionsType.DELETE_INFO_MAT.name]:
            return database.delete_info_mat(info_mat_id)
    raise HTTPException(status_code=401)


@router.put("/informational-material")
async def update_informational_material(_info_mat: InfoMatUpdateModel,
                                        user: User = Depends(verify_google_token)):
    for permission in user["permissions"]:
        if permission.permission_type in [PermissionsType.FULL.name,
                                          PermissionsType.EDIT_INFO_MAT.name]:
            info_mat_id = _info_mat.id
            return database.update_info_mat(info_mat_id, **_info_mat.attrs)
    raise HTTPException(status_code=401)


@router.post("/set-permission", response_model=Permission)
async def set_permission(target: EmailStr,
                         permission: PermissionsTypeModel,
                         days: int,
                         user: User = Depends(verify_google_token)):
    for _permission in user["permissions"]:
        if _permission.permission_type in [PermissionsType.FULL.name,
                                           PermissionsType.MANAGE_PERMISSIONS.name]:
            _user, _created = database.get_or_create_user(target)
            return database.register_permission(_user, permission.value,
                                                expiration_date=datetime.now() + timedelta(
                                                    days=days))
    raise HTTPException(status_code=401)


@router.post("/disable-user", response_model=bool)
async def update_informational_material(target: EmailStr,
                                        user: User = Depends(verify_google_token)):
    for _permission in user["permissions"]:
        if _permission.permission_type in [PermissionsType.FULL.name,
                                           PermissionsType.MANAGE_USERS.name]:
            _user, _created = database.get_or_create_user(target)
            _user.disable = True
            _user.save()
            return _user.disable
    raise HTTPException(status_code=401)


@router.post("/disable-user", response_model=bool)
async def disable_user(target: EmailStr,
                       user: User = Depends(verify_google_token)):
    for _permission in user["permissions"]:
        if _permission.permission_type in [PermissionsType.FULL.name,
                                           PermissionsType.MANAGE_USERS.name]:
            _user, _created = database.get_or_create_user(target)
            _user.disable = True
            _user.save()
            return True
    raise HTTPException(status_code=401)


@router.post("/enable-user", response_model=bool)
async def enable_user(target: EmailStr,
                      user: User = Depends(verify_google_token)):
    for _permission in user["permissions"]:
        if _permission.permission_type in [PermissionsType.FULL.name,
                                           PermissionsType.MANAGE_USERS.name]:
            _user, _created = database.get_or_create_user(target)
            _user.disable = False
            _user.save()
            return True
    raise HTTPException(status_code=401)
