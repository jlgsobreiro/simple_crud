from models.Account import Account
from models.Card import Card
from models.TransferHistory import TransferHistory
from repository.account import RepositorioAccount
from repository.card import RepositorioCard
from repository.transfer_history import RepositorioTransferHistory
from views.base_crud import SimpleCRUD


class CardView(SimpleCRUD):
    class Meta:
        meta = Card
        repo = RepositorioCard

    title = 'Card'



