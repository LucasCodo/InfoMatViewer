from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    admin_email: EmailStr
    GOOGLE_CLIENT_ID: str
    database: str = "vitrine"
    port: int = 5432
    password: str = "password_db"
    host: str = "db"
    user: str = "postgres"
    allowed_email_domains: list = ["@gmail.com", "@ufma.br", "@discente.ufma.br"]


APPSETTINGS = AppSettings()

DB_SETTINGS = dict(APPSETTINGS)
DB_SETTINGS.pop("admin_email")
DB_SETTINGS.pop("GOOGLE_CLIENT_ID")
DB_SETTINGS.pop("allowed_email_domains")
