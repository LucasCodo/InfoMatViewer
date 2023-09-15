from peewee import *
from time import time as timestamp
from pydantic_settings import BaseSettings, SettingsConfigDict
from enumerations import Permissions
import json


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    database: str
    port: int
    password: str
    host: str
    user: str


db_settings = dict(DatabaseSettings())
database = PostgresqlDatabase(**db_settings)
FORMATTING_DATE = "%d-%m-%Y"


class BaseModel(Model):
    time_stamp = IntegerField(default=int(timestamp()), null=True)

    class Meta:
        database = database


class JSONField(TextField):
    def db_value(self, value):
        return json.dumps(value)

    def python_value(self, value):
        if value is not None:
            return json.loads(value)


class Users(BaseModel):
    email = TextField(unique=True)
    disable = BooleanField(default=False)
    permissions = JSONField(default={[Permissions.VIEW_INFO_MAT]})


class InfoMat(BaseModel):
    title = TextField()
    author = JSONField()
    publication_year = TextField()
    cover_image = TextField()  # capa
    abstract = TextField()  # resumo
    matters = JSONField()  # assuntos
    tags = JSONField()  # tags
    number_of_pages = TextField()
    isbn = TextField()
    issn = TextField()
    typer = TextField()  # Tipo de material
    language = TextField(default="PT-BR")
    publisher = TextField()  # Editora
    volume = IntegerField()
    series = TextField()
    edition = TextField()
    reprint_update = TextField()


class Review(BaseModel):
    book = ForeignKeyField(InfoMat, backref='reviews')
    user = ForeignKeyField(Users, backref='reviews')
    rating = FloatField()


class InfoMatList(BaseModel):
    name = TextField()


class ListInforMats(BaseModel):
    infoMat = ForeignKeyField(InfoMat, backref='listInforMats')
    id_list = ForeignKeyField(InfoMatList, backref="listInforMats")

