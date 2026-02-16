from jose import JWTError, jwt
from .config import setting
from fastapi.security import oauth2
from datetime import timedelta, datetime, timezone
from . import schemas, models
from fastapi import HTTPException,status, Depends
from .db import get_db
from sqlalchemy.orm import Session
# from copy import deepcopy

OAuth2_schema = oauth2.OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY= setting.SECRET_KEY
ALGORITHM= setting.ALGORITHM
EXP_TIME_MINUTES= setting.EXP_TIME_MINUTES


def token_generation(data: dict) -> str:
    data_copy = data.copy()
    time_exp = datetime.now(timezone.utc) + timedelta(minutes=EXP_TIME_MINUTES)
    data_copy.update({"exp":time_exp})
    jwt_token = jwt.encode(data_copy, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token


def verify_token(bearer_token:str, error_response):
    try:
        payload = jwt.decode(token=bearer_token, key=SECRET_KEY, algorithms=[ALGORITHM])
        user_id =  payload.get("user_id")
        if user_id is None:
            raise error_response
        token_data = schemas.TokenData(id= user_id)
    except JWTError:
        raise error_response
    return token_data

def get_user(bearer_token : str = OAuth2_schema, db : Session = Depends(get_db)):
    error_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorised action', headers={"WWW_Authenticate":"Bearer"})
    token = verify_token(bearer_token=bearer_token,error_response=error_exception)
    user_data = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user_data