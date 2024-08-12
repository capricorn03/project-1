from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional , List
import time
from . import models , schemas
from .database import engine, get_db
from sqlalchemy.orm import Session


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import comments, likes, posts, users
from .database import engine
from .models import Base
from .config import settings

  # Create database tables 
models.Base.metadata.create_all(bind=engine) 

app = FastAPI(
    title="Social Media App API",
    version="1.0.0",
    description="API for a social media application.",
)





# Allow Cross-Origin Resource Sharing (CORS)
origins = ["*"]  # Replace with allowed origins if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Include routers
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(likes.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Social Media App API!"}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)
   