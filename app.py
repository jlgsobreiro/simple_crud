from datetime import timedelta

from flask import Flask, request, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, current_user
from flask_mongoengine import MongoEngine

from forms.Forms import LoginForm, RegisterForm
from models.Usuario import Usuario
from repository.usuario import RepositorioUsuarios

from views.setup import setup_crud_views

app = Flask(__name__)
app.config.from_pyfile("instance/config.py")
db = MongoEngine(app)

setup_crud_views(app)

bootstrap = Bootstrap5()
bootstrap.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)


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
    return render_template('main.html', links_nav_bar=app.links_nav_bar)


if __name__ == '__main__':
    app.run()
