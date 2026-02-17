from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..db import get_db
from typing import List
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostLikeCount])
def get_all_posts(db: Session = Depends(get_db)):
    # all_posts = db.query(models.Posts).all()
    all_posts = db.query(models.Posts, func.count(models.PostLikes.post_id).label("like_count")).outerjoin(models.PostLikes, models.PostLikes.post_id == models.Posts.id).group_by(models.Posts.id)
    return all_posts

@router.post("/",response_model=schemas.PostUserResponse)
def create_new_post(post : schemas.PostBase, db:Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    post_dict = post.model_dump(exclude_unset=True)
    new_post =models.Posts(owner_id=user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{post_id}/user", response_model=schemas.PostResponse)
def get_post_owner(post_id : int, db : Session = Depends(get_db), user : dict = Depends(oauth2.get_user)):
    requested_post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    return requested_post

@router.patch("/", response_model=schemas.PostUserResponse, status_code=status.HTTP_201_CREATED)
def update_post(paylod: schemas.UpdatePost, db: Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    orignal_post = db.query(models.Posts).filter(models.Posts.id == paylod.id).first()
    updated_post = paylod.model_dump(exclude_unset=True)
    if orignal_post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized Access")
    for key, value in updated_post.items():
        setattr(orignal_post, key, value)
    db.commit()
    db.refresh(orignal_post)

    return orignal_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, db : Session = Depends(get_db), user : models.Users = Depends(oauth2.get_user)):
    post = db.query(models.Posts).filter(models.Posts.id == post_id).first()
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorised request for deletion")
    db.delete(post)
    db.commit()
    