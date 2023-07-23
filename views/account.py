from models.Account import Account
from repository.account import RepositorioAccount
from views.base_crud import SimpleCRUD


class AccountView(SimpleCRUD):
    class Meta:
        meta = Account
        repo = RepositorioAccount

    title = 'Account'



