from fastapi import FastAPI, HTTPException, Header, Query, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.inmemory import InMemoryBackend
from schemas import AuthRequest, GetPostResponse, Post, Token
from utils import get_token, generate_random_string, encode_email

app = FastAPI()


@app.on_event("startup")
async def startup():
    FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

users = {}
posts = {}


def check_content_size(content: str):
    max_content_size = 1048576  # 1MB in bytes

    if len(content.encode('utf-8')) > max_content_size:
        raise HTTPException(status_code=400, detail="Content size too large")

    return content


@app.post("/signup")
async def signup(user_data: AuthRequest):
    print(user_data.email)
    users[user_data.email] = user_data
    posts[user_data.email] = []
    return {"message": "Signup successful", "data": user_data}


@app.post("/login")
async def login(login_data: AuthRequest):
    # Check if the email exists in user_data dictionary
    if login_data.email not in users:
        raise HTTPException(status_code=401, detail="Email not found")

    # Retrieve the user_info for the provided email
    user_info = users[login_data.email]

    # Check if the provided password matches the stored password
    if login_data.password != user_info.password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    return {"message": "Login successful", "token": encode_email(login_data.email)}


@app.post("/posts", response_model=Post)
async def add_post(post: Post, token: dict = Depends(get_token)):
    if token not in users:
        raise HTTPException(status_code=401, detail="Email not found")
    check_content_size(post.content)
    post.postId = generate_random_string(4)
    posts[token].append(post)
    print(posts)
    return post


@app.get("/posts", response_model=GetPostResponse)
@cache(expire=300)
async def get_post(token: dict = Depends(get_token)):
    if token not in users:
        raise HTTPException(status_code=401, detail="Email not found")
    post = posts[token]
    return GetPostResponse(email=token, posts=post)


@app.delete("/posts", response_model=GetPostResponse)
async def delete_post(postId: str = Query(), token: dict = Depends(get_token)):
    if token not in users:
        raise HTTPException(status_code=401, detail="Email not found")
    _posts = posts[token]
    for post in _posts:
        if post.postId == postId:
            _posts.remove(post)

    return GetPostResponse(email=token, posts=_posts)
