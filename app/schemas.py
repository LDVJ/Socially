from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List,Dict, Any

# Base schemas
class UserBase(BaseModel):
    name : str
    email : EmailStr
    username : str
    # mob_number: str
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

#create schema for user
class UserCreate(UserBase):
    password : str

# update user 
class UpdateUser(BaseModel):
    id: int
    username : str | None = None
    name : str | None = None

    model_config = {
        "from_attributes":True
    }

#update post
class UpdatePost(BaseModel):
    id: int
    title: str | None = None
    content : str | None = None
    tags : List[str] | None = None

    model_config = {
        "from_attributes":True
    }

# user response model
class UserResponse(UserBase): #independant schema 
    id : int
    created_at : datetime

# reponse of post along with user detail of who created it
class PostUserResponse(PostBase):
    id: int
    created_at : datetime
    updated_at : datetime | None = None

# reponse of post details along with like countt
class PostLikeCount(BaseModel):
    Posts: PostUserResponse
    like_count : int

# response of the posts along with the users detail who liked the post
class PostUserList(BaseModel):
    Posts: PostUserResponse
    like_count : int
    Users: List[UpdateUser]

# post response from the along with the user details based on relation of  models
class PostResponse(PostUserResponse): #independent schema
    owner_id : int
    owner : UserResponse


class UserPostResponse(UserBase):
    id: int
    created_at: datetime
    user_posts: List[PostUserResponse]

class PostLikes(BaseModel):
    id: int
    post_id : int
    user_id : int

# bearer token schemas 
class TokenData(BaseModel):
    id : int

class ValidToken(BaseModel):
    access_token : str
    token_type : str

#followed table
class Followers(BaseModel):
    id: int
    follower_uid: int
    followed_uid : int