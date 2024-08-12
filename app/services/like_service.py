# social_media_app/app/services/like_service.py
from sqlalchemy.orm import Session

from ..models import Like
from ..schemas import LikeBase, Like


def create_like(db: Session, like: LikeBase):
    db_like = Like(
        post_id=like.post_id,
        user_id=like.user_id,
    )
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def get_likes(db: Session):
    return db.query(Like).all()


def get_like(db: Session, like_id: int):
    return db.query(Like).filter(Like.id == like_id).first()


def delete_like(db: Session, like_id: int):
    db_like = db.query(Like).filter(Like.id == like_id).first()
    if not db_like:
        return None
    db.delete(db_like)
    db.commit()


