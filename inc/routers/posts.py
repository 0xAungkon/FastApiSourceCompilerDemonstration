from fastapi import APIRouter, HTTPException
from typing import List
from inc.models import Post, PostCreate

router = APIRouter()

# In-memory database for posts
posts_db: List[Post] = []
next_post_id = 1

@router.post("/posts/", response_model=Post, status_code=201)
async def create_post(post: PostCreate):
    global next_post_id
    new_post = Post(id=next_post_id, title=post.title, content=post.content)
    posts_db.append(new_post)
    next_post_id += 1
    return new_post

@router.get("/posts/", response_model=List[Post])
async def get_posts():
    return posts_db

@router.get("/posts/{post_id}", response_model=Post)
async def get_post(post_id: int):
    for post_in_db in posts_db:
        if post_in_db.id == post_id:
            return post_in_db
    raise HTTPException(status_code=404, detail="Post not found")
