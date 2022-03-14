from fastapi import APIRouter
from fastapi import Depends, FastAPI, status, HTTPException
from .db import metadata, database, engine, Article
from .schemas import ArticleSchema, MyArticleSchema, UserSchema
from typing import List
from .Token import get_current_user

router = APIRouter(
    tags=["Articles"],
    prefix="/articles"
)

####################### CRUD Operation 

#1 Create a new entry
@router.post('/', status_code=status.HTTP_201_CREATED)
async def insert_article(article:ArticleSchema):
    query = Article.insert().values(title = article.title, description = article.description)
    last_record_id = await database.execute(query)
    #to rebuild the response **article.dict() creates a key value pair from pydantic model and adds an id key 
    return {**article.dict(), "id":last_record_id}


#2 Read all entries 
#protected route by adding current_user:UserSchema = Depends(get_current_user) as query parms
@router.get('/', response_model=List[MyArticleSchema])
async def get_articles(current_user:UserSchema = Depends(get_current_user)):
    query = Article.select()
    return await database.fetch_all(query=query)


#3 Read one single entry
@router.get('/{id}', response_model=MyArticleSchema)
async def get_details(id:int, current_user:UserSchema = Depends(get_current_user)):
    query = Article.select().where(id == Article.c.id)
    myarticle = await database.fetch_one(query=query)

    if not myarticle:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    else:
        return {**myarticle}


#4 Update an entry
@router.put('/{id}', response_model=MyArticleSchema)
async def update_article(id:int, article:ArticleSchema):
    query = Article.update().where(Article.c.id == id).values(title=article.title, description=article.description)
    await database.execute(query)
    return {**article.dict(), "id":id}


#5  Delete an  entry
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(id:int):
    query = Article.delete().where(Article.c.id == id)
    await database.execute(query)
    return {"message":"Article deleted"}