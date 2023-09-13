from peewee import *
from time import time as timestamp
from pydantic_settings import BaseSettings, SettingsConfigDict
from secrets import token_hex
from typing import List
from datetime import date
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
