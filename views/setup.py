##Reserved_for_import
from views.sql_teste import sql_testeView
from views.user import UserView
from views.ModelTemplate import ModelTemplateView

links_nav_bar = [
    ('register', 'Registrar'),
    ('main', 'Main'),
    ('home', 'Home'),
    ('/userview', 'Usuarios'),
    ('/modeltemplateview', 'ModelTemplate'),
    ('/sql_testeview', 'sql_teste'),
##Reserved_for_links_nav_bar
]


def setup_crud_views(app):
    app.__setattr__("links_nav_bar", links_nav_bar)

    UserView.add_url_rule(app)
    ModelTemplateView.add_url_rule(app)
    sql_testeView.add_url_rule(app)
##Reserved_for_add_url_rule
