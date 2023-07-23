from repository.base_mongo import BaseMongo
from models.Account import Account


class RepositorioAccount(BaseMongo):
    class Meta:
        model = Account
