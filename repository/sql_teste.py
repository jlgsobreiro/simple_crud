from models.sql_teste import sql_teste
from repository.base_mongo import BaseMongo


class Repositorysql_teste(BaseMongo):
    class Meta:
        model = sql_teste
