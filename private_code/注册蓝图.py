

if __name__ == '__main__':

    from flask import Blueprint
    from base import create_app

    with create_app() as app:
        web = Blueprint('web', __name__)

        @app.route('/helloc')
        def helloc():
            return 'helloc'

        @web.route('/web_helloc')
        def web_helloc():
            return 'web_helloc'
        app.register_blueprint(web)
