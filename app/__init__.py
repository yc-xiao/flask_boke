from flask import Flask
from flask_login import LoginManager

loginmanager = LoginManager()

def create_app():
    # app = Flask(__name__, static_url_path='')
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    # register_router(app)
    register_blueprints(app)
    register_db(app)
    register_login(app)
    return app

def register_blueprints(app):
    from app.web.base import web
    app.register_blueprint(web)
    # from app.web2.base import web2
    # app.register_blueprint(web2)

def register_db(app):
    from app.models.base import db
    db.init_app(app)
    db.create_all(app=app)

def register_login(app):
    loginmanager.init_app(app)
    loginmanager.login_view = 'web.login'
    loginmanager.login_message = '请先登陆再访问'

def register_router(app):
    from werkzeug.routing import BaseConverter
    class RegexConverter(BaseConverter):
        def __init__(self, map, *args):
            import pdb;pdb.set_trace()
            self.map = map
            self.regex = args[0]
    app.url_map.converters['regex'] = RegexConverter
    '''
    @app.route('/view/<regex("[a-zA-Z0-9]+"):uuid>/')
    def view(uuid):
        """
        url: /view/1010000000125259/
        result: view uuid:1010000000125259
        """
        return "view uuid: %s" % (uuid)
    '''
