from flask_socketio import SocketIO as _SocketIO

class SocketIO(_SocketIO):
    def init_app(self, app, **kwargs):
        self._app = app
        super().init_app(app, **kwargs)

    def run(self, app=None, host=None, port=None, **kwargs):
        if not app:
            app = self._app
        super().run(app=app, host=host, port=port, **kwargs)

socketio = SocketIO()
