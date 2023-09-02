from typing import List
from pydantic import BaseModel


class AuthRequest(BaseModel):
    email: str
    password: str


class Post(BaseModel):
    postId: str = None
    title: str
    content: str


class Token(BaseModel):
    access_token: str


class GetPostResponse(BaseModel):
    email: str
    posts: List[Post]
