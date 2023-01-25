from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField, BooleanField, FloatField, IntegerField
from mongoengine.fields import StringField as MongoStringField, EmailField as MongoEmailField, BooleanField as MongoBooleanField, FloatField as MongoFloatField, IntField as MongoIntegerField
from wtforms.validators import DataRequired

from models.Produto import Produto
from models.Usuario import Usuario


class LoginForm(FlaskForm):
    user = StringField()
    password = PasswordField()

    remember_me = BooleanField()
    submit = SubmitField()


class RegisterForm(FlaskForm):
    usuario = StringField()
    senha = StringField()
    nome = StringField()
    sobrenome = StringField()
    email = EmailField()
    telefone = StringField()

    submit = SubmitField()


def add_form_fields_by_model(model_cls):
    def add_form_fields(form_cls):
        mongoengine_wtform_fields = {
            MongoEmailField: EmailField,
            MongoStringField: StringField,
            MongoFloatField: FloatField,
            MongoBooleanField: BooleanField,
            MongoIntegerField: IntegerField
        }

        for field_name, field_type in model_cls._fields.items():
            if field_type.__class__ not in mongoengine_wtform_fields:
                continue

            wtforms_field: Field = mongoengine_wtform_fields[field_type.__class__]
            field_instance = wtforms_field(label=field_name, validators=[DataRequired()])
            setattr(form_cls, field_name, field_instance)
        setattr(form_cls, 'submit', SubmitField())
        return form_cls

    return add_form_fields


@add_form_fields_by_model(Usuario)
class UsuarioForm(FlaskForm):
    def populated_obj(self):
        return self.populate_obj(Usuario)


@add_form_fields_by_model(Produto)
class ProdutoForm(FlaskForm):
    def populated_obj(self):
        return self.populate_obj(Produto)
