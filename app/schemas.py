from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass

class UserOut(BaseModel): # schema validator for Response when creating user
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut
    
    class Config: #sets the compatibility between the orm model(not just dictionary) and pydantic
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post 
    votes: int
      
    class Config: #sets the compatibility between the orm model(not just dictionary) and pydantic
        orm_mode = True

class UserCreate(BaseModel): # schema validator for creating user
    email: EmailStr
    password: str
        
class Login(BaseModel):
    email: EmailStr
    password: str
    
# schemas for token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

# Vote schema
class Vote(BaseModel):
    post_id: int
    vote_dir: conint(le=1)