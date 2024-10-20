from peewee import *

from settings import DB_CONNECTION

database = SqliteDatabase(DB_CONNECTION)