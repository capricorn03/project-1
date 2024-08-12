from sqlalchemy.orm import Session
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response, status
from ..database import get_db
from ..schemas import User, PostCreate, UserBase
from ..services import user_service
from .. import models , schemas


router = APIRouter(
    prefix= "/posts"
)

@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
   post_query = db.query(models.Post).filter(models.Post.id == id)
   
   if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
        
   post_query.update(post.model_dump(), synchronize_session=False)     
   db.commit()
   return post_query.first()




@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{id}")
def get_post(id : int, db: Session = Depends(get_db)):    
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was  not found")
    return post


@router.get("/" , response_model=List[schemas.Post])
def get_posts( db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)  
def create_posts( post : schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump()) # ** opretor is used to unpack the dictionary 
    db.add(new_post) # this will add the new_post object to the database
    db.commit()  # this will commit the changes to the database to save the new_post object
    db.refresh(new_post) # this will refresh the new_post object with the data from the database
    return new_post
   
   
