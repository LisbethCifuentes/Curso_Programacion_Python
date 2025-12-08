import os
from flask import current_app, g
from pymongo import MongoClient

def get_db():
    if "db" not in g:
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB_NAME")
        client = MongoClient(mongo_uri)
        g.db_client = client
        g.db = client[db_name]
    return g.db

def init_db(app):
    @app.teardown_appcontext
    def close_db(exception):
        client = g.pop("db_client", None)
        if client is not None:
            client.close()
