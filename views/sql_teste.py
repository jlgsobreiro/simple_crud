from models.sql_teste import sql_teste
from repository.sql_teste import Repositorysql_teste
from views.base_crud import SimpleCRUD


class sql_testeView(SimpleCRUD):
    class Meta:
        meta = sql_teste
        repo = Repositorysql_teste

    title = 'sql_teste'



