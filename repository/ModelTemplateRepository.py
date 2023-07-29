from models.ModelTemplate import ModelTemplate
from repository.base_mongo import BaseMongo


class RepositoryModelTemplate(BaseMongo):
    class Meta:
        model = ModelTemplate
