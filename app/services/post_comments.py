from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, oauth2, models
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db import get_db
from typing import List

router = APIRouter(
    prefix="/comment",
    tags=["Comments"]
)


@router.post("/", response_model=schemas.CommentResponse)
def create_comment(payload : schemas.CreatePostComment, db : Session = Depends(get_db), current_user : models.Users = Depends(oauth2.get_user)):
    check_post = db.get(models.Posts, payload.post_id)
    if not check_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested post not found")
    new_comment = models.PostComments(post_id = payload.post_id, content = payload.content, comment_uid = current_user.id)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get("/{pid}",response_model=List[schemas.CommentResponse])
def get_all_post_comments(pid: int, db : Session = Depends(get_db), current_user : models.Users = Depends(oauth2.get_user)):
    valid_post = db.get(models.Posts, pid)
    if not valid_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not found")
    