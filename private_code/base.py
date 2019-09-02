from contextlib import contextmanager
from flask import Flask

config = {
    'host': 'localhost',
    'port': 9999,
    'debug': True
}

def get_attrs(app, key):
    return [attr for attr in dir(app) if attr.find(key) != -1]

@contextmanager
def create_app():
    app = Flask(__name__, static_url_path='')
    yield app
    print('http://{host}:{port}'.format(**config))
    print(app.url_map)
    print(app.view_functions)
    app.run(**config)

def route(app):
    app.add_url_rule('/', view_func=lambda:'helloc')
    urls = get_attrs(app, 'url')
    # print(urls)

if __name__ == '__main__':
    with create_app() as app:
        route(app)
