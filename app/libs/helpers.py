from celerys.tasks.task_send_email import send_email
from app.libs.logging_helper import app_logger
from functools import wraps
from flask import request
import pdb

def ttry(step=1):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kw):
            try:
                if step != 1:
                    pdb.set_trace()
                results = func(*args, **kw)
                return results
            except Exception as e:
                print('函数名称：', func.__name__)
                print('函数参数：', *args, **kw)
                print('错误提示：',e.args)
                pdb.set_trace()
                return func(*args, **kw)
        return inner
    return wrapper

def log_info(step=1):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kw):
            app_logger.info(f'''请求url:{request.url}\t请求方式:{request.method}\tip: {request.remote_addr}\tuser_agent:{request.user_agent}''')
            # [print({i: getattr(request, i)}) for i in dir(request)]
            results = func(*args, **kw)
            return results
        return inner
    return wrapper

def send_error_email(step=1):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kw):
            try:
                results = func(*args, **kw)
            except Exception as e:
                data = {
                    'subject': '告诉你一个好消息,你的服务器好像挂了!',
                    'to_addr': '395015856@qq.com',
                    'content': e.args[0]
                }
                send_email.delay(**data)
                raise e
            return results
        return inner
    return wrapper
