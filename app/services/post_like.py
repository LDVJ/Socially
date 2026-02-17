from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..db import get_db

router = APIRouter(
   prefix= "/postlikes",
   tags=['Like post']
)


@router.post("/{pid}", response_model= dict, status_code = status.HTTP_201_CREATED)
def like_post(pid: int, db: Session = Depends(get_db), user: models.Users = Depends(oauth2.get_user)):
    check_like = db.query(models.PostLikes).filter(models.PostLikes.post_id == pid, models.PostLikes.user_id == user.id).first()
    if check_like is None:
        new_like = models.PostLikes(post_id = pid, user_id = user.id)
        db.add(new_like)
        db.commit()
        return {"message":"Post Liked Successfully"}
    else:
        db.delete(check_like)
        db.commit()
        return {"message":"Post Like removed successfully"}
