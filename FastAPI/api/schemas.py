import imp
from pydantic import BaseModel
from typing import Optional

class ArticleSchema(BaseModel):
    # id:int  -- no need for this since the db models has it as PK and will autoincrement
    title:str
    description:str

class MyArticleSchema(ArticleSchema): #use as response model to specify which of the fields alone should be returned
    title:str
    description:str


class UserSchema(BaseModel):
    username:str
    password:str

class MyUserSchema(BaseModel):
    id:int 
    username:str    


class LoginSchema(BaseModel):
    username:str
    password:str

class TokenData(BaseModel):
    username: Optional[str] = None