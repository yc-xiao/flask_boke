from app.libs.helpers import ttry
from app.libs.helpers import log_info
from flask import Blueprint

class _Blueprint(Blueprint):
    def route(self, rule, **options):
        """
            重写route方法，加上异常处理。
            可以记录日志，可以进入断点模式。
        """
        def decorator(f):
            endpoint = options.pop("endpoint", f.__name__)
            # f = ttry(1)(f)
            f = log_info()(f) # 添加日志记录
            self.add_url_rule(rule, endpoint, f, **options)
            return f
        return decorator

Blueprint = _Blueprint
web = Blueprint('web', __name__)
