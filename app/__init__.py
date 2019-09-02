from flask import Flask
from app.models.base import db

def create_app():
    # app = Flask(__name__, static_url_path='')
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    register_blueprints(app)
    register_db(app)
    return app

def register_blueprints(app):
    from app.web.base import web
    app.register_blueprint(web)
    # from app.web2.base import web2
    # app.register_blueprint(web2)

def register_db(app):
    db.init_app(app)
    db.create_all(app=app)
