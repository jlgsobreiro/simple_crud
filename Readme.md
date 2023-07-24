Para construir o servidor no docker, execute o seguinte comando:
```make build```

Para rodar o servidor no docker, execute o seguinte comando:
```make start```

Para parar o servidor no docker, execute o seguinte comando:
```make stop```

É possivel rodar o servidor sem o docker, para isso, execute o seguinte comando:
```flask run```

Como utilizar o SimpleCRUD:

Crie um modelo na pasta models, seguindo o exemplo do arquivo User.py
```
from bson import ObjectId
from mongoengine import Document
from mongoengine.fields import *

from models.BaseModel import BaseModel


class Usuario(Document, BaseModel):
    usuario = StringField(required=True)
    senha = StringField(required=True)
    nome = StringField(required=True)
    sobrenome = StringField(required=True)
    email = EmailField(required=True)
    telefone = StringField(required=True)

    def get_all(self):
        return Usuario.objects()

    def instance_reference(self):
        return Usuario

    def format_self(self):
        pass

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return ObjectId(self.id).__str__()

 ```
Crie um repositorio na pasta repository, seguindo o exemplo do arquivo usuario.py
```
from models.Usuario import Usuario
from repository.base_mongo import BaseMongo


class RepositorioUsuarios(BaseMongo):
    class Meta:
        model = Usuario
 ```
Crie uma view na pasta view, seguindo o exemplo do arquivo user.py
```
from models.Usuario import Usuario
from repository.usuario import RepositorioUsuarios
from views.base_crud import SimpleCRUD


class UserView(SimpleCRUD):
    class Meta:
        meta = Usuario
        repo = RepositorioUsuarios

    title = 'Usuarios'
 ```
No arquivo Forms.py na pasta forms, crie uma entrada no fim do arquivo como o seguinte exemplo:
```
@add_form_fields_by_model(Usuario)
class UsuarioForm(FlaskForm):
    def populated_obj(self):
        return self.populate_obj(Usuario)
```

Para utilizar o SimpleCRUD, vá ao arquivo setup.py e adicione o repositorio criado na lista de repositorios, seguindo o exemplo:
``` 
.
.
.
from views.user import UserView

links_nav_bar = [
    .
    .
    .
    ('/userview', 'Usuarios')
]
def setup_crud_views(app):
    app.__setattr__("links_nav_bar", links_nav_bar)
    
    .
    .
    .
    UserView.add_url_rule(app)
```

É utilizado um mapeamento entre os campos do mongoengine e os campos do wtforms.
Caso esteja utilizando um campo que não esteja mapeado no dicionario, adicione o registro no dicionario, seguindo o exemplo:
```
mongoengine_wtform_fields = {
            MongoEmailField: EmailField,
            MongoStringField: StringField,
            MongoFloatField: FloatField,
            MongoBooleanField: BooleanField,
            MongoIntegerField: IntegerField,
            MongoCampoDesejado: CampoDesejadoField
        }
```

