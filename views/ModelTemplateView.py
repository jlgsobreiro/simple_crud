from models.ModelTemplate import ModelTemplate
from repository.ModelTemplateRepository import RepositoryModelTemplate
from views.base_crud import SimpleCRUD


class ExempleModelView(SimpleCRUD):
    class Meta:
        meta = ModelTemplate
        repo = RepositoryModelTemplate

    title = 'ModelTemplate'



