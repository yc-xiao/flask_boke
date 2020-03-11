from celerys.tasks.task_send_email import send_email
from app.libs.logging_helper import app_logger
from functools import wraps
from flask import request
import traceback
import pymongo
import time
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

def add_log(data):
    client = pymongo.MongoClient()
    db = client.logs
    db.log.insert(data)

def log_info(step=1):
    def wrapper(func):
        @wraps(func)
        def inner(*args, **kw):
            remote_ip = request.environ.get('HTTP_X_REAL_IP') or '127.0.0.1'
            referer = request.environ.get('HTTP_X_REFERER')
            data = {
                'url': request.url,
                'method': request.method,
                'remote_ip': remote_ip,
                'referer': referer,
                'user_agent': str(request.user_agent),
                'time': time.strftime('%Y-%m-%d %H:%S:%M',time.localtime(time.time())),
            }
            app_logger.info('''请求url:{url}\t请求方式:{method}\tremote_ip: {remote_ip}\tuser_agent:{user_agent}'''.format(**data))
            add_log(data)
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
                error_infos = traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)
                data = {
                    'subject': '告诉你一个好消息,你的服务器好像挂了!',
                    'to_addr': '395015856@qq.com',
                    'content': '\n'.join(error_infos)
                }
                send_email.delay(**data)
                raise e
            return results
        return inner
    return wrapper
