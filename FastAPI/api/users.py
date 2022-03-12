from fastapi import APIRouter
from fastapi import Depends, FastAPI, status, HTTPException
from .db import User, metadata, database, engine, Article
from .schemas import UserSchema, MyUserSchema
from typing import List
from passlib.hash import pbkdf2_sha256

router = APIRouter(
    tags=["users"],
    prefix="/users"
)


@router.post('/',  status_code=status.HTTP_201_CREATED, response_model=MyUserSchema,)
async def create_user(user:UserSchema):
    hashed_password = pbkdf2_sha256.hash(user.password)
    query = User.insert().values(username = user.username, password = hashed_password) 
    last_record_id = await database.execute(query)
    return {**user.dict(), "id":last_record_id}

@router.get('/', response_model=List[MyUserSchema])
async def get_users():
    query = User.select()
    return await database.fetch_all(query=query)