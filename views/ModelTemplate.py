from models.ModelTemplate import ModelTemplate
from repository.ModelTemplate import RepositoryModelTemplate
from views.base_crud import SimpleCRUD


class ModelTemplateView(SimpleCRUD):
    class Meta:
        meta = ModelTemplate
        repo = RepositoryModelTemplate

    title = 'ModelTemplate'



