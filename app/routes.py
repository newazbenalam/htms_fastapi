from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from sqlalchemy.orm import Session
from functools import lru_cache
from app.database import get_db
from app.models import User, Post
from app.schemas import UserBase, PostBase
from typing import Annotated, List

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/users/", status_code=status.HTTP_201_CREATED, response_model=UserBase)
def create_user(user: UserBase, db: db_dependency):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    return db_user

@lru_cache(maxsize=128)
@router.get("/users/", status_code=status.HTTP_200_OK,  response_model=List[UserBase])
def read_users(db: db_dependency):
    users = db.query(User).all()
    return users

@lru_cache(maxsize=128)
@router.get("/users/{user_id}")
def get_user_by_email(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")
  
@router.post("/post/", status_code=status.HTTP_201_CREATED, response_model=PostBase)
def create_post(postData: PostBase, db: db_dependency):
    db_post = Post(**postData.model_dump())
    db.add(db_post)
    db.commit()
    return db_post

@lru_cache(maxsize=128)
@router.get("/post/", status_code=status.HTTP_200_OK,  response_model=List[PostBase])
def read_post(db: db_dependency):
    return db.query(Post).all()

@lru_cache(maxsize=128)
@router.get("/post/{post_id}", status_code=status.HTTP_200_OK, response_model=PostBase)
def get_post_by_id(post_id: int, db: db_dependency):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        return post
    raise HTTPException(status_code=404, detail="User not found")