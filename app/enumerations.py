from enum import Enum, auto


# Defina um enum para as permissões
class Permissions(Enum):
    VIEW_INFO_MAT = auto()
    CREATE_INFO_MAT = auto()
    EDIT_INFO_MAT = auto()
    DELETE_INFO_MAT = auto()
    MANAGE_USERS = auto()
