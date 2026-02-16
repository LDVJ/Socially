from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..db import get_db
from .. import schemas, models, utilities
from typing import List


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=List[schemas.UserResponse],status_code=status.HTTP_200_OK)
def get_user(search : str ="", limit: int=10, skip: int = 0, db : Session = Depends(get_db)):
    all_users = db.query(models.Users).filter(models.Users.name.contains(search)).limit(limit=limit).offset(offset=skip).all()
    return all_users

@router.post("/",response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    Hashed_password = utilities.create_hash_password(user.password)
    user.password = Hashed_password
    new_user = models.Users(**user.model_dump(exclude_unset=True))
    db.add(new_user)
    try: 
        db.commit()
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig)
        if "users_username_key" in error_msg:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Username already exist")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already Exist")
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}/posts", response_model=schemas.UserPostResponse)
def get_user_posts(user_id : int, db : Session = Depends(get_db)):
    user_post_details = db.query(models.Users).filter(models.Users.id == user_id).first()
    return user_post_details