from bson import ObjectId
from mongoengine import Document
from mongoengine.fields import *

from models.BaseModel import BaseModel


class sql_teste(Document, BaseModel):
    field_string = StringField(required=True)
    int_field = IntField(required=True)
    float_field = FloatField(required=True)
    bool_field = BooleanField(required=False)

    def format_self(self):
        self.bool_field = self.bool_field == 'y'
        self.float_field = float(self.float_field)
        self.int_field = int(self.int_field)

    def get_all(self):
        return sql_teste.objects()

    def instance_reference(self):
        return sql_teste

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def persist_data(self):
        self.save()

    def get_id(self):
        return ObjectId(self.id).__str__()
