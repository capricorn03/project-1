from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from datetime import datetime

from pydantic.types import conint

# class name should be Starts with Capital letter in pyhton
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    #no need of these as we extended PostBase class 
    # title: str
    # content: str
    # published: bool  
    
    created_at: datetime 
    class Config:
        from_attributes = True

# class UserOut(BaseModel):
#     id: int
#     email: EmailStr
#     created_at: datetime

#     class Config:
#         from_attributes = True


# class PostOut(BaseModel):
#     Post: Post
#     votes: int

#     class Config:
#         from_attributes = True


# class UserCreate(BaseModel):
#     email: EmailStr
#     password: str


# class UserLogin(BaseModel):
#     email: EmailStr
#     password: str


# class Token(BaseModel):
#     access_token: str
#     token_type: str


# class TokenData(BaseModel):
#     id: Optional[str] = None


# # class Vote(BaseModel):
# #     post_id: int
# #     dir: conint(le=1)