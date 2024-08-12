# social_media_app/app/routers/likes.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..schemas import Like, LikeBase
from ..services import like_service

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
)


@router.post("/", response_model=Like)
async def create_like(like: LikeBase, db: Session = Depends(get_db)):
    return like_service.create_like(db, like)


@router.get("/", response_model=List[Like])
async def get_likes(db: Session = Depends(get_db)):
    return like_service.get_likes(db)


@router.get("/{like_id}", response_model=Like)
async def get_like(like_id: int, db: Session = Depends(get_db)):
    like = like_service.get_like(db, like_id)
    if not like:
        raise HTTPException(
            status_code=404, detail="Like not found"
        )
    return like


@router.delete("/{like_id}")
async def delete_like(like_id: int, db: Session = Depends(get_db)):
    like_service.delete_like(db, like_id)
    return {"message": "Like deleted successfully"}

