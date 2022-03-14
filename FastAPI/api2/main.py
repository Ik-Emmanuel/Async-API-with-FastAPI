from fastapi import FastAPI, HTTPException, status
from .models import Article_Pydantic, ArticleIn_Pydantic, Article
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
import json
from typing import List
from pydantic import BaseModel


app = FastAPI()

class Status(BaseModel):
    message: str


#Read environment variable
with open ('vars.json', 'r') as variables:
    env_vars = json.loads(variables.read()) 

#MySQL database url 
DATABASE_URL = f"{env_vars['DB']}://{env_vars['DB_USER']}:{env_vars['DB_PASSWORD']}@localhost/articleorm"

###############################################################################################

##### CRUD operations  

# 1. Get all 
@app.get('/articles', response_model=List[Article_Pydantic])
async def get_article():
    return await Article_Pydantic.from_queryset(Article.all())

# 2. Get one 
@app.get('/articles/{id}', response_model=Article_Pydantic, responses={404:{"model":HTTPNotFoundError}})
async def get_detail(id:int):
    return await Article_Pydantic.from_queryset_single(Article.get(id=id))

#3 Create 
@app.post('/articles', response_model=Article_Pydantic)
async def insert_article(article:ArticleIn_Pydantic):
    article_obj = await  Article.create(**article.dict(exclude_unset=True))
    return await Article_Pydantic.from_tortoise_orm(article_obj)

#4 Update data
@app.put('/articles/{id}', response_model=Article_Pydantic, responses={404:{"model":HTTPNotFoundError}})
async def update(id:int, article:ArticleIn_Pydantic):
    await Article.filter(id=id).update(**article.dict(exclude_unset=True))
    return await Article_Pydantic.from_queryset_single(Article.get(id=id))


#5 Delete data
@app.delete('/articles/{id}',  response_model=Status, responses={404:{"model":HTTPNotFoundError}})
async def delete_article(id:int):
    deleted_article = await Article.filter(id=id).delete()

    if not deleted_article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"Article {id} not found")
    return Status(message= f"Deleted article {id}")


###################################################################################
register_tortoise(
    app, 
    db_url = DATABASE_URL,
    modules ={"models":["api2.models"]},
    generate_schemas = True, 
    add_exception_handlers = True
)