from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class settings(BaseSettings):
    DB_USER : str
    DB_PWD : str
    DB_HOST : str
    DB_PORT : str
    DB_NAME : str
    SECRET_KEY : str
    ALGORITHM : str
    EXP_TIME_MINUTES : int

    @property
    def cleaned_pwd(self):
        return self.DB_PWD.strip()


    model_config = SettingsConfigDict(
        env_file=os.path.join(os.getcwd(), ".env"),
        extra="ignore"
    )

setting = settings()
