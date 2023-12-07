from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    admin_email: str
    database: str
    port: int
    password: str
    host: str
    user: str
    GOOGLE_CLIENT_ID: str


APPSETTINGS = AppSettings()

DB_SETTINGS = dict(APPSETTINGS)
DB_SETTINGS.pop("admin_email")
DB_SETTINGS.pop("GOOGLE_CLIENT_ID")
