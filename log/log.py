1.新增目录?
    app
        libs(库)
        models(数据层)
        static(静态层)
        web(web应用,通过蓝图挂在app应用上)
        api(api应用,通过蓝图挂在app应用上)
    main.py # 启动文件


2.蓝图对象类似app对象?
    app.web.base.py
        from flask import Blueprint
        web = Blueprint('web', __name__)
        @web.route('/')
        def helloc():
            return 'helloc'

    app.__init__.py
        app = Flask()
        app.config.from_object('app.setting') # 加载配置信息
        app.register_blueprint(web)           # 注册蓝图

3.
