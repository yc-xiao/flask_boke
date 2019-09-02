# 应用上下文 AppContext  => LocalStack => LocalProxy => Flask()  => app
# 请求上下文 RequestContext => LocalStack => LocalProxy => Request() => request
from flask import Flask, current_app
from werkzeug.local import LocalStack

class _LocalStack(object):
    pass

_app_ctx_stack = LocalStack()

class _AppContext(object):
    def __init__(self, app):
        self.app = app
    def __enter__(self):
        self.push()
        return self

    def __exit__(self, *args):
        self.pop()
        return False

    def push(self):
        print('push')
        _app_ctx_stack.push(self)

    def pop(self):
        print('pop')
        _app_ctx_stack.pop(self)

class _Flask(object):
    def __init__(self, app):
        self.app = app

    def app_context(self):
        return _AppContext(self.app)

def _main(app):
    _app = _Flask(app)
    ctx = _app.app_context()
    ctx.push()
    ctx.pop()

def main(app):
    with app.app_context():
        print(current_app)

if __name__ == '__main__':
    # print(current_app) 没有app对象会直接报错
    app = Flask(__name__)
    main(app)
    # _main(app)
