from enum import Enum


# Defina um enum para as permissões
class PermissionsType(str, Enum):
    FULL = "FULL"
    VIEW_INFO_MAT = "VIEW_INFO_MAT"
    CREATE_INFO_MAT = "CREATE_INFO_MAT"
    EDIT_INFO_MAT = "EDIT_INFO_MAT"
    DELETE_INFO_MAT = "EDIT_INFO_MAT"
    MANAGE_USERS = "EDIT_INFO_MAT"
    MANAGE_PERMISSIONS = "MANAGE_PERMISSIONS"


PermissionsTypeList = PermissionsType.__members__.keys()
