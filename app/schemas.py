from pydantic import BaseModel, EmailStr, conint 
from typing import Optional


class PostSchema(BaseModel):
    """Schema for creating or updating a post."""
    title: str
    content: str
    published: bool = True
class UserSchema(BaseModel):
    """Schema for reading user data."""
    id: int
    email: EmailStr

class Post(BaseModel):
    """Schema for reading a post, compatible with ORM models."""
    id: int  # Added `id` for reading posts (usually database-generated)
    title: str
    content: str
    published: bool
    owner_id: int  # Ensures the owner_id is included in the response
    owner: UserSchema
    class Config:
        from_attributes = True  # Enables ORM compatibility


class PostOut(BaseModel):
    post: Post
    votes: int

    class Config:
        from_attributes = True  # Enables ORM compatibility

class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    Password: str  # Password field should be lowercase




    class Config:
        from_attributes = True  # Enables ORM compatibility


class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for access tokens."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token payload."""
    id: Optional[str] = None
class Vote(BaseModel):
    post_id: int
    dir:conint(le=1)
    

