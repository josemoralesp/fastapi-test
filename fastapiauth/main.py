# pylint: disable=missing-final-newline
from typing import Awaitable
from types import ClassMethodDescriptorType
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from graphene import ObjectType, List, String, Schema, Mutation, Field
from graphql.execution.executors.asyncio import AsyncioExecutor
from starlette.graphql import GraphQLApp
from schemas import UserSchema
from models import User
from passlib.hash import bcrypt
import json


app = FastAPI()

JWT_SECRET = 'myjwtsecret'

User_Pydantic_List = pydantic_queryset_creator(User)
User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User,
                                         name='UserIn',
                                         exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


class Query(ObjectType):

    user_list = None
    get_users = List(UserSchema)
    hello = String(name=String(default_value="World"))

    def resolve_hello(self, info, name):
        return 'Hello ' + name

    async def resolve_get_users(self, info):
        users = await User_Pydantic_List.from_queryset(User.all())
        return json.loads(users.json())


class CreateUser(Mutation):

    user = Field(UserSchema)

    class Arguments:
        username = String(required=True)
        password_hash = String(required=True)

    async def mutate(self, info, username, password_hash):
        user_obj = User(username=username,
                        password_hash=bcrypt.hash(password_hash))
        await user_obj.save()
        new_user = await User_Pydantic.from_tortoise_orm(user_obj)
        return CreateUser(user=new_user)


class Mutation(ObjectType):
    create_user = CreateUser.Field()


app.add_route("/", GraphQLApp(
    schema=Schema(query=Query, mutation=Mutation),
    executor_class=AsyncioExecutor,
    # dependencies=Depends(oauth2_scheme)
    )
)


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['main']},
    generate_schemas=True,
    add_exception_handlers=True,
)

