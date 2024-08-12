# social_media_app/app/services/comment_service.py
from sqlalchemy.orm import Session

from ..models import Comment
from ..schemas import CommentCreate, Comment


def create_comment(db: Session, comment: CommentCreate):
    db_comment = Comment(
        content=comment.content,
        post_id=comment.post_id,
        user_id=comment.user_id,
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comments(db: Session):
    return db.query(Comment).all()


def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()


def update_comment(db: Session, comment_id: int, comment: CommentCreate):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        return None
    db_comment.content = comment.content
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not db_comment:
        return None
    db.delete(db_comment)
    db.commit()


