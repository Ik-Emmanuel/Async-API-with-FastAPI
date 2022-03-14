import re
from fastapi import APIRouter, Depends
from fastapi import status, HTTPException
from .db import User, database
from typing import List
from passlib.hash import pbkdf2_sha256
from .Token import create_access_token
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter(
    tags=["Auth"],
    prefix="/login"
)


@router.post('/',)
async def login(request: OAuth2PasswordRequestForm = Depends()):
    query = User.select().where(User.c.username == request.username)
    user = await database.fetch_one(query)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not pbkdf2_sha256.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")
    else:
        access_token = create_access_token(
            data={"sub": user.username},
        )
        return {"access_token": access_token, "token_type": "bearer"}

