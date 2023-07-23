from datetime import timedelta

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, current_user, AnonymousUserMixin
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_mongoengine.wtf import model_form
from flask_mongoengine.wtf.models import ModelForm
from flask_wtf import FlaskForm
from wtforms.fields import *

from forms.Forms import LoginForm, RegisterForm
from models.Usuario import Usuario
from repository.usuario import RepositorioUsuarios
from views.account import AccountView
from views.card import CardView
from views.produto import ProdutoView
from views.transfer_history import TransferHistoryView
from views.user import UserView

app = Flask(__name__)
app.config.from_pyfile("instance/config.py")
db = MongoEngine(app)


links_nav_bar = [
    ('register', 'Registrar'),
    ('main', 'Main'),
    ('home', 'Home'),
    # (user_table_view_endpoint.replace('/', ''), 'Usuarios')
    ('/userview', 'Usuarios'),
    ('/produtoview', 'Produtos'),
    ('/accountview', 'Account'),
    ('/transferhistoryview', 'Transfer History'),
    ('/cardview', 'Card'),
]

app.__setattr__("links_nav_bar", links_nav_bar)

bootstrap = Bootstrap5()
bootstrap.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

user_view = UserView
user_view.links_nav_bar = links_nav_bar
user_view.add_url_rule(app)

produto_view = ProdutoView
produto_view.links_nav_bar = links_nav_bar
produto_view.add_url_rule(app)

account_view = AccountView
account_view.links_nav_bar = links_nav_bar
account_view.add_url_rule(app)

trasnfer_history_view = TransferHistoryView
trasnfer_history_view.links_nav_bar = links_nav_bar
trasnfer_history_view.add_url_rule(app)

card_view = CardView
card_view.links_nav_bar = links_nav_bar
card_view.add_url_rule(app)


@login_manager.user_loader
def load_user(user_id):
    user = RepositorioUsuarios().find_one(id=user_id)
    return user


@app.route('/', methods=["POST", "GET"])
def home():
    home_form = LoginForm()
    if current_user.is_authenticated:
        flash(current_user, 'success')
        return redirect(url_for('main'))
    if request.method == "POST":
        user: Usuario = RepositorioUsuarios().find_one(usuario=home_form.user.data)
        if user:
            if user.senha == home_form.password.data:
                login_user(user, home_form.remember_me, timedelta(days=7))
                flash('teste', 'success')
                return redirect(url_for('main'))
        else:
            flash('teste', 'error')
    return render_template('home.html', form=home_form)


@app.route('/register', methods=["POST", "GET"])
def register():
    print(f"usuarios: {Usuario.objects()}")
    register_form = RegisterForm()
    if request.method == "POST":
        usuario = Usuario()
        register_form.populate_obj(usuario)
        try:
            usuario.save()
            flash('parece que foi')
            return redirect(url_for('home'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('home.html', form=register_form)


@app.route('/main', methods=["POST", "GET"])
def main():
    return render_template('main.html', links_nav_bar=links_nav_bar)


# @app.route('/usuarios', methods=["POST", "GET"])
# def usuarios():
#     usuarios_data = RepositorioUsuarios().find()
#     permissoes = ['create', 'edit', 'delete']
#     print(usuarios_data)
#     return render_template("table.html", title='Usuarios', links_nav_bar=links_nav_bar, data=usuarios_data, permissions=permissoes)
#
#
# @app.route('/usuarios/editar/<id_item>', methods=["POST", "GET"])
# def usuarios_editar(id_item):
#     user = RepositorioUsuarios().find_one(id=id_item)
#     edit_form = model_form(instance=user)
#     form = edit_form(request.form)
#     if request.method == "POST":
#         edit_form.populate_obj(user)
#         user.save()
#     return render_template("edit.html", title='Usuarios', links_nav_bar=links_nav_bar, form=form)
#
#
# @app.route('/usuarios/apagar/<id_item>', methods=["POST", "GET"])
# def usuarios_apagar(id_item):
#     flash('apagando')
#     RepositorioUsuarios().find_one(id=id_item).delete()
#     print(id_item)
#     return redirect(url_for('usuarios'))
#
#
# @app.route('/usuarios/criar', methods=["POST", "GET"])
# def usuarios_criar():
#     return render_template("crud.html", title='Usuarios', links_nav_bar=links_nav_bar)


@app.route('/produtos', methods=["POST", "GET"])
def produtos():
    return render_template("crud.html", title='produtos', links_nav_bar=links_nav_bar)


@app.route('/contas', methods=["POST", "GET"])
def contas():
    return render_template("crud.html", title='contas', links_nav_bar=links_nav_bar)


@app.route('/inventario', methods=["POST", "GET"])
def inventario():
    return render_template("crud.html", title='Inventário', links_nav_bar=links_nav_bar)


if __name__ == '__main__':
    app.run()
