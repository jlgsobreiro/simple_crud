from bson import ObjectId
from mongoengine import Document
from mongoengine.fields import *

from models.BaseModel import BaseModel


class Account(Document, BaseModel):
    owner = StringField(required=True)
    amount = StringField(required=True)
    card = StringField(required=True)

    def get_all(self):
        return Account.objects()

    def instance_reference(self):
        return Account

    def format_self(self):
        pass

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return ObjectId(self.id).__str__()
