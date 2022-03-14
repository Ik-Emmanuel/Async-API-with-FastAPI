from unicodedata import name
from unittest.util import _MAX_LENGTH
from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator 


#both db models and pydantic model 


class Article(models.Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.CharField(max_length=255)

    class PydanticMeta:
        pass



### Example of Model with computations

# class City(models.Model):
#     id = fields.IntField(pk=True)
#     name = fields.CharField(max_length=255)
#     timezone = fields.CharField(max_length=255)

#     def current_time(self) -> str:
#         r = requests.get(f'https//timezone/{self.timezone}')
#         current_time = r.json()['datetime']
#         return current_time
#     class PydanticMeta:
#         #specifies all the computed fields to be retured in your API for the given model
#         computed = ('current_time',)



# Tortoise helps with creation of pydantic models creator from database models 
Article_Pydantic = pydantic_model_creator(Article, name="Article")
ArticleIn_Pydantic = pydantic_model_creator(Article, name="ArticleIn", exclude_readonly=True)