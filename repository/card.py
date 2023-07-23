from models.Card import Card
from repository.base_mongo import BaseMongo
from models.Account import Account


class RepositorioCard(BaseMongo):
    class Meta:
        model = Card
