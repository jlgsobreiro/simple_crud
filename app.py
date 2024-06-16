import json
import os
from datetime import timedelta

from flask import Flask, request
from fixtures import run_fixtures
import pymongo as pymongo
from mysql import connector

app = Flask(__name__)
app.config.from_pyfile("instance/config.py")


@app.route('/dbs', methods=["GET"])
def dbs():
    # return list of dbs
    return str(db)


@app.route('/dbs/<db>', methods=["GET"])
def db(db):
    # check if db exists
    # return db description or error
    return str(db)


@app.route('/dbs/<db>/<table>', methods=["GET"])
def table(db, table):
    # check if db exists
    # check if table exists
    # return table description or error
    return str(table)


@app.route('/delete', methods=["DELETE"])
def delete():
    pymongo_client = pymongo.MongoClient(
        host=app.config['MONGODB_SETTINGS']['host'],
        port=app.config['MONGODB_SETTINGS']['port'],
        username=app.config['MONGODB_SETTINGS']['username'],
        password=app.config['MONGODB_SETTINGS']['password']
    )

    request_body = request.json
    target_db = request_body.get('db')
    target_table = request_body.get('table')
    target_table_exist = pymongo_client[target_db][target_table].find_one()
    if not target_table_exist:
        return "Table does not exist", 400

    # check if db exists
    # check if table exists
    # delete table
    # return success or failed
    return "OK"


@app.route('/update', methods=["UPDATE"])
def update():
    pymongo_client = get_mongo_conn()

    request_body = request.json
    target_db = request_body.get('db')
    target_table = request_body.get('table')
    fields = request_body.get('fields')
    target_table_exist = pymongo_client[target_db][target_table].find_one()
    if not target_table_exist:
        return "Table does not exist", 400

    # check if db exists
    # check if table exists
    # update table with fields
    # return success or failed
    return "OK"


@app.route('/read', methods=["GET"])
def read():
    pymongo_client = get_mongo_conn()

    request_body = request.json
    target_db = request_body.get('db')
    target_table = request_body.get('table')
    target_table_exist = pymongo_client[target_db][target_table].find_one()
    if not target_table_exist:
        return "Table does not exist", 400

    # check if db exists
    # check if table exists
    # return table data
    return "OK"


@app.route('/insert', methods=["POST"])
def insert():
    pymongo_client = get_mongo_conn()

    request_body = request.json
    target_db = request_body.get('db')
    target_table = request_body.get('table')
    fields = request_body.get('fields')
    force_create = request_body.get('force_create')
    target_table_object = None
    if target_db == 'mongo':
        target_table_object = pymongo_client[target_db][target_table]
        for keys in fields.keys():
            print(keys)
            if "fk" in keys:
                print(f"foreign key {keys}")
                fk_found = get_foreign_key(keys, fields[keys])
                if fk_found is None:
                    return "Foreign key not found", 400
                fields[keys] = fk_found
        if target_table_object is not None:
            inserted_value = target_table_object.insert_one(fields).inserted_id
            print(inserted_value)
            return json.dumps({"id": str(inserted_value)}), 200
    elif target_db == 'mysql':
        mysql_client = get_mysql_conn()
        target_table_object = mysql_client.cursor()
        target_table_object.execute(f"SHOW TABLES LIKE '{target_table}';")
        print(target_table_object.fetchone())
        if target_table_object.fetchone() is None:
            if force_create:
                type_map = {
                    int: 'INT',
                    str: 'VARCHAR(255)',
                    bool: 'BOOLEAN',
                    float: 'FLOAT'
                }
                print({', '.join([f"{key} {type_map.get(type(fields[key]), 'VARCHAR(255)')}" for key in fields.keys()])})
                target_table_object.execute(f'''
                CREATE TABLE IF NOT EXISTS {target_table} (
                id INT AUTO_INCREMENT PRIMARY KEY,
               {', '.join([f"{key} {type_map.get(type(fields[key]), 'VARCHAR(255)')}" for key in fields.keys()])}
                );''')
            else:
                return "Table does not exist", 400

        if target_table_object is not None:
            for keys in fields.keys():
                print(keys)
                if "fk" in keys:
                    print(f"foreign key {keys}")
                    fk_found = get_foreign_key(keys, fields[keys])
                    if fk_found is None:
                        return "Foreign key not found", 400
                    fields[keys] = fk_found
            print(f"INSERT INTO {target_table}")
            print(f"({', '.join(fields.keys())}) VALUES")
            print(f"({', '.join([str(x) for x in fields.values()])});")
            inserted_value = target_table_object.execute(f"INSERT INTO {target_table} ({', '.join(fields.keys())}) VALUES ({', '.join([str(x) for x in fields.values()])});")
            print(inserted_value)
            return json.dumps({"id": str(inserted_value)}), 200

    # print("fk" in fields.keys())


    # check if db exists
    # check if table exists
    # insert data into table
    # return success or failed
    return "OK"


def get_mongo_conn():
    pymongo_client = pymongo.MongoClient(
        host=app.config['MONGODB_SETTINGS']['host'],
        port=app.config['MONGODB_SETTINGS']['port'],
        username=app.config['MONGODB_SETTINGS']['username'],
        password=app.config['MONGODB_SETTINGS']['password']
    )
    return pymongo_client


def get_mysql_conn():
    mysql_client = connector.connect(
        host=app.config['MYSQL_SETTINGS']['host'],
        port=app.config['MYSQL_SETTINGS']['port'],
        password=app.config['MYSQL_SETTINGS']['password'],
        user=app.config['MYSQL_SETTINGS']['username'],
        database=app.config['MYSQL_SETTINGS']['db']
    )
    return mysql_client


def get_foreign_key(key: str, fk: dict):
    print(key)
    print(fk)
    target_db = key.split("__")[1]
    target_table = key.split("__")[2]
    print(f"target_db: {target_db}, target_table: {target_table}")
    if target_db == 'mongo':
        foreign_key = get_mongo_conn()[target_db][target_table].find_one(fk)
        if foreign_key is None:
            return None
        print(foreign_key.get('_id'))
        return str(foreign_key.get('_id'))
    elif target_db == 'mysql':
        mysql_client = get_mysql_conn()
        target_table_object = mysql_client.cursor()
        target_table_object.execute(f"SELECT id from {target_table} limit 1;")

        foreign_key = target_table_object.fetchone()
        print(foreign_key)
        if foreign_key is None:
            return None

        return foreign_key


if __name__ == '__main__':
    # if os.getenv('ENVIRONMENT') == 'development':
    run_fixtures()
    app.run()
