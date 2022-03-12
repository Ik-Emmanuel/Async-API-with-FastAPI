from sqlalchemy import (
    Column,
    Integer,
    MetaData,
    String,
    Table, 
    create_engine
)
import json
from databases import Database

with open ('vars.json', 'r') as variables:
    env_vars = json.loads(variables.read())  

DATABASE_URL = f"{env_vars['DB']}://{env_vars['DB_USER']}:{env_vars['DB_PASSWORD']}@localhost/asyncfastapi"



metadata = MetaData()
Article = Table(
    "article",
    metadata,
    Column("id", Integer, primary_key=True), 
    Column("title", String(100)), 
    Column("description",  String(500)), 
)

engine = create_engine(DATABASE_URL)
database = Database(DATABASE_URL)