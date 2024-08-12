# social_media_app/app/routers/comments.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import Comment, CommentCreate, CommentBase
from ..services import comment_service

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
)


@router.post("/", response_model=Comment)
async def create_comment(
    comment: CommentCreate, db: Session = Depends(get_db)
):
    return comment_service.create_comment(db, comment)


@router.get("/", response_model=List[Comment])
async def get_comments(db: Session = Depends(get_db)):
    return comment_service.get_comments(db)


@router.get("/{comment_id}", response_model=Comment)
async def get_comment(
    comment_id: int, db: Session = Depends(get_db)
):
    comment = comment_service.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(
            status_code=404, detail="Comment not found"
        )
    return comment


@router.put("/{comment_id}", response_model=Comment)
async def update_comment(
    comment_id: int,
    comment: CommentBase,
    db: Session = Depends(get_db),
):
    return comment_service.update_comment(db, comment_id, comment)


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int, db: Session = Depends(get_db)
):
    comment_service.delete_comment(db, comment_id)
    return {"message": "Comment deleted successfully"}


