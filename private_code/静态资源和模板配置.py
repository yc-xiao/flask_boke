'''
    app
        templates
        static
        web
            base.py
            templates
    app默认静态资源和模板路径为app目录下的static和templates
    # 可以改变路径，填相对路径
    app = Flask(__name__, templates='web/templates') 默认路径为template
    web = Blueprint('web', __name__, templates='templates') 默认路径为空
    当由多个模板路径时，可以认为模板页面会放在一个集合内，重复名称会出错。
    静态资源static最后会被添加到路由内,self.add_url_rule('/static', view_func=self.send_static_file)
    send_static_file该函数用于发送文件数据
'''
from flask.helpers import send_from_directory
from base import create_app
import os

if __name__ == '__main__':
    BASE_PATH = os.path.dirname(__file__)
    STATIC_PATH = os.path.join(BASE_PATH, 'static')
    with create_app() as app:
        @app.route('/uploads/<path:filename>')
        def download_file(filename):
            # http://localhost:9999/uploads/base.py
            return send_from_directory(STATIC_PATH,
                                       filename)
