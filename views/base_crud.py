from flask import render_template, request, flash, redirect, url_for
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from mongoengine import Document
import wtforms.fields as wtf_fields
from wtforms.validators import DataRequired
from forms.Forms import UserForm

from repository.base_mongo import BaseMongo




class SimpleCRUD:
    permissoes = ['create', 'edit', 'delete']
    links_nav_bar = []
    title = ''
    form = None
    table = None

    @classmethod
    def table_view(cls):
        _id = request.form.get('id', '')

        cls.table = cls.Meta.repo().get_all_to_dict_list()
        print(cls.table)
        try:
            print('opa')
            return render_template('crud.html',
                                   title=cls.title,
                                   links_nav_bar=cls.links_nav_bar,
                                   form=cls.form,
                                   table=cls.table,
                                   permissions=cls.permissoes,
                                   cls_endpoint=cls.__name__.lower(),
                                   id=_id)
        except Exception as e:
            print('Erro: ', e)
            return render_template('not_found.html')

    @classmethod
    def edit_view(cls, id_item=None):
        edit_data = cls.Meta.repo().find_one(id=id_item)
        edit_form = model_form(edit_data)
        form = edit_form(request.form)
        print(id_item)
        if request.method == "PUT":
            edit_form.populate_obj(edit_data)
            edit_data.save()
        return render_template("edit.html", title=cls.title, links_nav_bar=cls.links_nav_bar, form=form)

    @classmethod
    def delete_view(cls, id_item=None):
        flash('apagando')
        cls.Meta.repo().find_one(id=id_item).delete()
        print(id_item)
        return cls.table_view()

    @classmethod
    def create_view(cls):
        form = UserForm(cls.Meta.meta())
        # form = model_form(cls.Meta.meta())

        return render_template("crud.html", title=cls.title, links_nav_bar=cls.links_nav_bar, form=form)

    @classmethod
    def url_rule_table(cls):
        return f'/{cls.__name__.lower()}', cls.table_view

    @classmethod
    def url_rule_edit(cls):
        return f'/{cls.__name__.lower()}/edit/<id_item>', cls.edit_view

    @classmethod
    def url_rule_delete(cls):
        return f'/{cls.__name__.lower()}/delete/<id_item>', cls.delete_view

    @classmethod
    def url_rule_create(cls):
        return f'/{cls.__name__.lower()}/create', cls.create_view

    @classmethod
    def add_url_rule(cls, app):
        table_view_endpoint, table_view = cls.url_rule_table()
        edit_view_endpoint, edit_view = cls.url_rule_edit()
        create_view_endpoint, create_view = cls.url_rule_create()
        delete_view_endpoint, delete_view = cls.url_rule_delete()
        app.add_url_rule(table_view_endpoint, endpoint=table_view_endpoint, view_func=table_view, methods=['POST', 'GET', 'PUT', 'DELETE'])
        app.add_url_rule(edit_view_endpoint, endpoint=edit_view_endpoint, view_func=edit_view, methods=['POST', 'GET', 'PUT', 'DELETE'])
        app.add_url_rule(create_view_endpoint, endpoint=create_view_endpoint, view_func=create_view, methods=['POST', 'GET', 'PUT', 'DELETE'])
        app.add_url_rule(delete_view_endpoint, endpoint=delete_view_endpoint, view_func=delete_view, methods=['POST', 'GET', 'PUT', 'DELETE'])
