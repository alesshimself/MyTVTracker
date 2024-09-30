from flask import Flask
from flask_login import LoginManager

from config import Config
from .milvus_utils import connect_to_milvus, create_collection

milvus_collection = None
login = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    login.init_app(app)
    login.login_view = 'login'

    connect_to_milvus(app.config['MILVUS_HOST'], app.config['MILVUS_PORT'])
    global milvus_collection
    milvus_collection = create_collection("tv_shows_users", dim=1024)

    from app import routes

    return app
