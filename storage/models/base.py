from peewee import Model

import storage.storage

class BaseModel(Model):
    class Meta:
        database = storage.storage.database