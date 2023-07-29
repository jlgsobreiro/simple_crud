##Reserverd_for_import
from views.account import AccountView
from views.card import CardView
from views.produto import ProdutoView
from views.transfer_history import TransferHistoryView
from views.user import UserView
from views.ModelTemplateView import ExempleModelView

links_nav_bar = [
    ('register', 'Registrar'),
    ('main', 'Main'),
    ('home', 'Home'),
    ('/userview', 'Usuarios'),
    ('/produtoview', 'Produtos'),
    ('/accountview', 'Account'),
    ('/transferhistoryview', 'Transfer History'),
    ('/cardview', 'Card'),
    ('/exemplemodelview', 'ExempleModel'),
##Reserverd_for_links_nav_bar
]


def setup_crud_views(app):
    app.__setattr__("links_nav_bar", links_nav_bar)

    UserView.add_url_rule(app)
    ProdutoView.add_url_rule(app)
    AccountView.add_url_rule(app)
    TransferHistoryView.add_url_rule(app)
    CardView.add_url_rule(app)
    ExempleModelView.add_url_rule(app)
##Reserverd_for_add_url_rule