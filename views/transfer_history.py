from models.Account import Account
from models.TransferHistory import TransferHistory
from repository.account import RepositorioAccount
from repository.transfer_history import RepositorioTransferHistory
from views.base_crud import SimpleCRUD


class TransferHistoryView(SimpleCRUD):
    class Meta:
        meta = TransferHistory
        repo = RepositorioTransferHistory

    title = 'Transfer History'



