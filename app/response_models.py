from typing import Any

from pydantic import BaseModel, EmailStr, model_validator
from datetime import datetime
from app.enumerations import PermissionsTypeList
from typing import Literal


class InfoMat(BaseModel):
    id: int
    title: str
    author: list
    publication_year: str
    cover_image: str  # capa
    abstract: str  # resumo
    matters: list  # assuntos
    tags: list  # tags
    number_of_pages: str
    isbn: str
    issn: str
    typer: str  # Tipo de material
    language: str
    publisher: str  # Editora
    volume: int
    series: str
    edition: str
    reprint_update: str


class InfoMatBasic(BaseModel):
    id: int
    title: str
    author: list
    cover_image: str
    rating: float


class InfoMatBasicWithOutRating(BaseModel):
    id: int
    title: str
    author: list
    cover_image: str


class InfoMatList(BaseModel):
    id: int
    name: str
    observable: bool
    listInfoMats: list[InfoMatBasicWithOutRating]


class InfoMatListPost(BaseModel):
    name: str
    public: bool
    listIDsInfoMats: list[int]


class JsonQuery(BaseModel):
    query: dict[str, str] | dict[str, list[dict]]


class InfoMatUpdateModel(BaseModel):
    id: int
    attrs: dict[str, Any]


class Permission(BaseModel):
    expiration_date: datetime | None
    permission_type: str


class User(BaseModel):
    id: int
    hd: str
    email: EmailStr
    name: str
    picture: str
    given_name: str
    family_name: str
    locale: str = "pt-BR"
    permissions: list[Permission]


class PermissionsTypeModel(BaseModel):
    value: Literal[
        "FULL",
        "VIEW_INFO_MAT",
        "CREATE_INFO_MAT",
        "EDIT_INFO_MAT",
        "EDIT_INFO_MAT",
        "EDIT_INFO_MAT",
        "MANAGE_PERMISSIONS",
    ]

    @model_validator(mode="after")
    def validate_permission(self):
        if self.value not in PermissionsTypeList:
            raise ValueError(f'Permission {self.value} not Exist!')
        return self
