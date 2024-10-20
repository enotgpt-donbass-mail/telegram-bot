import datetime
import uuid

from peewee import CharField, BigIntegerField, DateTimeField, BooleanField

from storage.models.base import BaseModel


class User(BaseModel):
    telegram_id = BigIntegerField(unique=True, primary_key=True)
    login = CharField(default=uuid.uuid4)
    username = CharField(null=True)
    first_name = CharField(null=True)
    last_name = CharField(null=True)
    index = CharField(null=True)
    office_id = CharField(null=True)
    post_name = CharField(null=True)
    phone_number = CharField(null=True)
    created_at = DateTimeField(default=datetime.datetime.now)
    is_banned = BooleanField(default=False)

