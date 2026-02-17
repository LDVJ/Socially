from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utilities, oauth2
from ..db import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Login"]
)

@router.post("/login",response_model=schemas.ValidToken)
def login_user( user_creds : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    valid_user = db.query(models.Users).filter(models.Users.email == user_creds.username).first()
    if valid_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    is_valid_password = utilities.verify_hash_password(user_creds.password, valid_user.password)
    if not is_valid_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Credentials")
    access_token = oauth2.token_generation({"user_id":valid_user.id})

    return {
        "access_token" :  access_token,
        "token_type" : "bearer"
    }



