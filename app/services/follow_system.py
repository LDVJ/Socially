from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db import get_db
from .. import models, schemas, oauth2
from typing import List

router = APIRouter(
    prefix="/follow",
    tags=["Follow"]
)

@router.post("/{uid}")
def follow_user(uid: int, db : Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    check_valid_follow = db.get(models.Users.id == uid)
    if not check_valid_follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found for following")
    new_follower = models.FollowList(follwed_uid = uid, follower_uid = user.id)
    followed_name = db.query(models.Users.username).filter(models.Users.id == uid).scalar() # retuns the exact value of the column 
    # followed_name = db.query(models.Users.username).filter(models.Users.id == uid).first() # retuns the value of the column but in tupple formaat
    try: 
        db.add(new_follower)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise IntegrityError
    
    return {
        "message":f"You Started Following {followed_name}"
    }

# @router.get("/followers", response_model=List[schemas.])