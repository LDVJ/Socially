from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, oauth2
from ..db import get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_all_posts(db: Session = Depends(get_db)):
    all_posts = db.query(models.Posts).all()
    return all_posts

@router.post("/",response_model=schemas.PostUserResponse)
def create_new_post(post : schemas.PostBase, db:Session = Depends(get_db), user : dict = Depends(oauth2.get_user)):
    post_dict = post.model_dump(exclude_unset=True)
    new_post =models.Posts(owner_id=user.id, **post_dict)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
