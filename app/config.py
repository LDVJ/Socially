from pydantic_settings import BaseSettings, SettingsConfigDict


class settings(BaseSettings):
    DB_USER : str
    DB_PWD : str
    DB_HOST : str
    DB_PORT : str
    DB_NAME : str

    model_config = SettingsConfigDict(env_file=".env")

setting = settings()
