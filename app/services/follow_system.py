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

@router.post("/{uid}", status_code=status.HTTP_201_CREATED)
def follow_user(uid: int, db : Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    check_valid_follow = db.query(models.Users).filter(models.Users.id == uid).first()
    if not check_valid_follow:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found for following")
    if check_valid_follow.id == user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Reuqest. Trying to follow itself")
    new_follower = models.FollowList(followed_uid = uid, follower_uid = user.id)
    followed_name = db.query(models.Users.username).filter(models.Users.id == uid).scalar() # retuns the exact value of the column 
    # followed_name = db.query(models.Users.username).filter(models.Users.id == uid).first() # retuns the value of the column but in tupple formaat
    try: 
        db.add(new_follower)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You are alredy following the user")
    
    return {
        "message":f"You Started Following {followed_name}"
    }

@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
def remove_follow(uid : int, db : Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    valid_user = db.get(models.Users, uid)
    if not valid_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested User not found")
    valid_request = db.query(models.FollowList).filter(models.FollowList.followed_uid == uid and models.FollowList.follower_uid == user.id).first()
    print(valid_request)
    if not valid_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad Request")
    db.delete(valid_request)
    db.commit()

@router.get("/{uid}/followers", response_model=List[schemas.UserResponse])
def get_followers(uid : int, db: Session = Depends(get_db), search = "",limit = 10,skip = 0):
    valid_user = db.query(models.Users).filter(models.Users.id == uid).first()
    if not valid_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
    followers =db.query(models.Users).join(models.FollowList, models.FollowList.follower_uid == models.Users.id).filter(models.FollowList.followed_uid == uid).filter(models.Users.username.contains(search)).limit(limit=limit).offset(offset=skip).all()
    return followers

@router.get("/{uid}/followed", response_model=List[schemas.UserResponse])
def get_followed(uid : int, db: Session = Depends(get_db), search = "",limit = 10,skip = 0):
    valid_user = db.query(models.Users).filter(models.Users.id == uid).first()
    if not valid_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not found")
    followers =db.query(models.Users).join(models.FollowList, models.FollowList.followed_uid == models.Users.id).filter(models.FollowList.follower_uid == uid).filter(models.Users.username.contains(search)).limit(limit=limit).offset(offset=skip).all()
    return followers