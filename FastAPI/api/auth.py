import re
from fastapi import APIRouter
from fastapi import Depends, FastAPI, status, HTTPException
from .db import User, metadata, database, engine, Article
from .schemas import MyUserSchema, UserSchema, LoginSchema
from typing import List
from passlib.hash import pbkdf2_sha256

router = APIRouter(
    tags=["Auth"],
    prefix="/login"
)


@router.post('/', response_model=MyUserSchema )
async def login(request:LoginSchema):
    query = User.select().where(User.c.username == request.username)
    user = await database.fetch_one(query)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not pbkdf2_sha256.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    else:
        return user

