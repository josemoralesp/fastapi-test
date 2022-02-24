# pylint: disable=missing-final-newline
import typing
import strawberry
from strawberry.types import Info
from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from strawberry.fastapi import GraphQLRouter
from starlette.requests import Request
from starlette.websockets import WebSocket
from strawberry.permission import BasePermission
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
import odoo_env
from schemas import UserSchema, UserInputSchema
from models import User
from passlib.hash import bcrypt
import json


app = FastAPI()

User_Pydantic_List = pydantic_queryset_creator(User)
User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User,
                                         name='UserIn',
                                         exclude_readonly=True)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class IsAuthenticated(BasePermission):
    message = "User is not authenticated"

    def has_permission(self, source: typing.Any, info: Info, **kwargs) -> bool:
        request: typing.Union[Request, WebSocket] = info.context["request"]

        print(request.headers)
        print(request.query_params)
        if "Authorization" in request.headers:
            pass
            # return authenticate_header(request)

        if "auth" in request.query_params:
            pass
            # return authenticate_query_params(request)

        return True

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return 'Hello World'

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def get_users(self, info: Info) -> typing.List[UserSchema]:
        conn = odoo_env.odoo_env()
        partners = conn.execute('res.partner', 'search_read', [], ['name', 'email', 'phone'], 0, 100)
        # users = await User_Pydantic_List.from_queryset(User.all())
        return [User(**i) for i in partners]

@strawberry.type
class Mutation:

    @strawberry.field
    async def create_user(self, user: UserInputSchema) -> UserSchema:
        user_obj = User(username=user.username,
                        password_hash=bcrypt.hash(user.password_hash))
        await user_obj.save()
        new_user = await User_Pydantic.from_tortoise_orm(user_obj)
        return UserSchema(**new_user.dict())


schema = strawberry.Schema(Query, Mutation)
graphql_app = GraphQLRouter(
  schema
)
app.include_router(graphql_app, prefix="/graphql")


register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['models']},
    generate_schemas=True,
    add_exception_handlers=True,
)
