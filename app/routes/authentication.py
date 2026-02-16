from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import schemas, oauth2
from ..db import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=["Login"]
)

@router.post("/login",response_model=schemas.UserResponse)
def login_user( user : OAuth2PasswordRequestForm, db: Session = Depends(get_db)):

    pass


