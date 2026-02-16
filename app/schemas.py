from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List,Dict, Any

# Base schemas
class UserBase(BaseModel):
    name : str
    email : EmailStr
    username : str

    model_config = {
        "from_attributes":True
    }

class PostBase(BaseModel):
    title: str
    content : str | None =None
    tags : List[str] | None = None
    model_config = {
        "from_attributes" : True
    }

#input schema for user

class UserCreate(UserBase):
    password : str


class UserResponse(UserBase): #independant schema 
    id : int
    created_at : datetime

class PostUserResponse(PostBase):
    id: int
    created_at : datetime
    updated_at : datetime | None = None

class PostResponse(PostUserResponse): #independent schema
    owner_id : int
    owner : UserResponse

class UserPostResponse(UserBase):
    id: int
    created_at: datetime
    user_posts: List[PostUserResponse]

class ValidUser(BaseModel):
    email : EmailStr
    password : str

class TokenData(BaseModel):
    id : int

class ValidToken(BaseModel):
    access_token : str
    token_type : str

