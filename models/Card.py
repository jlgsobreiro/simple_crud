from bson import ObjectId
from mongoengine import Document
from mongoengine.fields import *

from models.BaseModel import BaseModel


class Card(Document, BaseModel):
    nome_portador = StringField(required=True)
    numero_do_cartao = StringField(required=True)
    cvv = StringField(required=True)
    validade = StringField(required=True)
    conta_associada = StringField(required=True)

    def get_all(self):
        return Card.objects()

    def instance_reference(self):
        return Card

    def format_self(self):
        pass

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return ObjectId(self.id).__str__()
