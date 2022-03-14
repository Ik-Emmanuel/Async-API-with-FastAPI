import json
from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table, 
    create_engine
)

from databases import Database


with open ('vars.json', 'r') as variables:
    env_vars = json.loads(variables.read())  

DATABASE_URL = f"{env_vars['DB']}://{env_vars['DB_USER']}:{env_vars['DB_PASSWORD']}@localhost/asyncfastapi"


###STEP 1
metadata = MetaData()

#STEP 2  DB Tables to be created
Article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True), 
    Column("title", String(100)), 
    Column("description",  String(500)), 
)

User = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True), 
    Column("username", String(100)), 
    Column("password",  String(200)), 
)

#STEP 3
engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)



#STEP 4 in main.py

# Create your tables  
# metadata.create_all(engine)

# app = FastAPI()


#Set up your db connection 

# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def startup():
#     await database.disconnect()