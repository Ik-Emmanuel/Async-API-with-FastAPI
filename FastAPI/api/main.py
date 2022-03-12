from fastapi import FastAPI
from .db import metadata, database, engine
from . import articles, users

##########################################################################################

metadata.create_all(engine)

app = FastAPI()

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def startup():
    await database.disconnect()

###################################################################


app.include_router(articles.router)
app.include_router(users.router)