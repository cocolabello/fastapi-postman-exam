from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()

# Q1- Route GET /ping
@app.get("/ping", response_class=PlainTextResponse)
async def ping():
    return PlainTextResponse(content="pong", status_code=200)

# Q2- Route GET /home
@app.get("/home", response_class=HTMLResponse)
async def home():
    return HTMLResponse(content="<html><body><h1>Welcome home!</h1></body></html>", status_code=200)

# Q3- Exception handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if exc.status_code == 404:
        return HTMLResponse(content="<html><body><h1>404 NOT FOUND</h1></body></html>", status_code=404)
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

# Q4 - Route POST /posts
class Post(BaseModel):
    author: str
    title: str
    content: str
    creation_datetime: datetime
posts: List[Post] = [Post(author="Corina", title="Sample Post", content="This is mypost.", creation_datetime=datetime.now())]

@app.post("/posts", response_model=List[Post], status_code=status.HTTP_201_CREATED)
async def create_posts(posts_data: List[Post]):
    global posts
    posts.extend(posts_data)
    return posts

# Q5 - Route GET /posts
@app.get("/posts", response_model=List[Post], status_code=status.HTTP_200_OK)
async def get_posts():
    return posts

# Q6 - Route PUT /posts
@app.put("/posts", response_model=List[Post], status_code=status.HTTP_200_OK)
async def update_or_create_posts(posts_data: List[Post]):
    global posts
    for new_post in posts_data:
        for i, existing_post in enumerate(posts):
            if existing_post.title == new_post.title:
                if (existing_post.author != new_post.author or
                        existing_post.content != new_post.content or
                        existing_post.creation_datetime != new_post.creation_datetime):
                    posts[i] = new_post
                break
        else:
            posts.append(new_post)
    return posts
