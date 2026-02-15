from pydantic_settings import BaseSettings


class settings(BaseSettings):
    DB_USER : str
    DB_PWD : str
    DB_HOST : str
    DB_PORT : str
    DB_NAME : str

    class config:
        env_file = ".env"

setting = settings()
