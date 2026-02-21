from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from ..db import get_db

router = APIRouter(
   prefix= "/postlikes",
   tags=['Like post']
)


@router.post("/{pid}", response_model= dict, status_code = status.HTTP_201_CREATED)
def like_post(pid: int, db: Session = Depends(get_db), user: models.Users = Depends(oauth2.get_user)):
    check_post = db.get(models.Posts, pid)
    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found")
    
    check_like = db.query(models.PostLikes).filter(models.PostLikes.post_id == pid, models.PostLikes.user_id == user.id).first()
    if check_like is None:
        new_like = models.PostLikes(post_id = pid, user_id = user.id)
        db.add(new_like)
        db.commit()
        return {"message":"Post Liked Successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Already Liked Post")

@router.delete("/{pid}", status_code= status.HTTP_204_NO_CONTENT)
def remove_like(pid :int, db : Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    check_post = db.get(models.Posts, pid)
    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not fonud")
    check_like = db.query(models.PostLikes).filter(models.PostLikes.post_id == pid).first()
    if not check_like:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Like not found")
    db.delete(check_like)
    db.commit()

@router.get("/{pid}", response_model=schemas.PostLikeCount)
def get_post_likes_count(pid : int, db: Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    check_post = db.get(models.Posts, pid)
    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found")
    
    post_likes = db.query(models.PostLikes, func.count(models.PostLikes.id).label("like_count")).outerjoin(models.Posts.id, models.PostLikes.post_id == models.Posts.id).group_by(models.Posts.id)
    return post_likes

@router.get("/{pid}/users", response_model=schemas.PostUserList)
def get_user_list(pid : int, db: Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    check_post = db.query(models.Posts).filter(models.Posts.id == pid).first()
    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found")
    liked_users = db.query(models.Users).join(models.PostLikes, models.PostLikes.user_id == models.Users.id).filter(models.PostLikes.post_id == pid).all()
    # liked_users = (
    #     db.query(models.Users)
    #     .join(models.PostLikes, models.PostLikes.user_id == models.Users.id)
    #     .filter(models.PostLikes.post_id == pid)
    #     .all()
    # )
    like_count = len(liked_users)
    return {
        "Posts": check_post,
        "like_count": like_count,
        "Users": liked_users
    }
