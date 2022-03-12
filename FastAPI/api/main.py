from typing import Optional
from fastapi import FastAPI

app = FastAPI()

data = [
    {"title":"First"},
    {"title":"Second"},
    {"title":"Third"},
]

@app.get('/') #path operation decorator 
def Index(): #path operation function 
    return {"message": "Hello IK again from FASTAPI!"}

@app.get('/articles/{id}') #path with path parameter
def get_articles(id:int): 
    return {"message": {'id': id}}


@app.get('/articles/')
def get_articles(skip:int = 0, limit:int=20, q:Optional[str] =None): 
    #Query parameters same as http://localhost:8000/articles/?skip=0&limit=20
    return {"message": {'data': data[skip: skip + limit], 'Query':q }}