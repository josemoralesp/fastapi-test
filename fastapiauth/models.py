# pylint: disable=missing-final-newline
from typing import Awaitable
from passlib.hash import bcrypt
from tortoise import fields
from tortoise.models import Model
import asyncio

class User(Model):

    id = fields.IntField(pk=True)
    name = fields.CharField(50, unique=True)
    phone = fields.CharField(50, unique=True)
    email = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    @classmethod
    async def get_all_users(cls):
        return cls.all()

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)
