from app import create_app

app = create_app()

# @app.before_request
# def before_request():
#     from flask import request
#     print(request.remote_addr, request.user_agent, request.url)

if __name__ == '__main__':
    # app.run()
    from app.websockets.base import socketio
    socketio.init_app(app)
    socketio.run(app)
