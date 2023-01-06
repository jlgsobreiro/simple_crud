from flask_wtf import FlaskForm
from wtforms import Field
from wtforms.fields import StringField, PasswordField, EmailField, SubmitField, BooleanField
from mongoengine.fields import StringField as MongoStringField, EmailField as MongoEmailField
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
            MongoStringField: StringField
        }

        for field_name, field_type in model_cls._fields.items():
            print(field_type)
            print(mongoengine_wtform_fields.keys())
            if field_type.__class__ not in mongoengine_wtform_fields:
                continue

            wtforms_field: Field = mongoengine_wtform_fields[field_type.__class__]
            field_instance = wtforms_field(label=field_name, validators=[DataRequired()])
            setattr(form_cls, field_name, field_instance)
        setattr(form_cls, 'submit', SubmitField())
        return form_cls

    return add_form_fields


@add_form_fields_by_model(Usuario)
class UserForm(FlaskForm):
    pass


@add_form_fields_by_model(Produto)
class ProdutoForm(FlaskForm):
    pass
