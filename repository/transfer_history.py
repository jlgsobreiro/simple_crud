from models.TransferHistory import TransferHistory
from repository.base_mongo import BaseMongo
from models.Account import Account


class RepositorioTransferHistory(BaseMongo):
    class Meta:
        model = TransferHistory
