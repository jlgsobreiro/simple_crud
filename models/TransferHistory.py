from bson import ObjectId
from mongoengine import Document
from mongoengine.fields import *

from models.BaseModel import BaseModel


class TransferHistory(Document, BaseModel):
    sender = StringField(required=True)
    receiver = StringField(required=True)
    amount = StringField(required=True)
    status = StringField(required=True)
    datetime = StringField(required=True)


    def get_all(self):
        return TransferHistory.objects()

    def instance_reference(self):
        return TransferHistory

    def format_self(self):
        pass

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return ObjectId(self.id).__str__()
