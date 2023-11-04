from pydantic import BaseModel
from typing import Optional, Union


class InfoMat(BaseModel):
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
    title: str
    author: list
    cover_image: str
    rating: float


class InfoMatBasicWithOutRating(BaseModel):
    title: str
    author: list
    cover_image: str


class InfoMatList(BaseModel):
    name: str
    observable: bool
    listInfoMats: list[InfoMatBasicWithOutRating]


class InfoMatListPost(BaseModel):
    name: str
    public: bool
    listIDsInfoMats: list[int]


class JsonQuery(BaseModel):
    query: dict[str, str] | dict[str, list[dict]]
