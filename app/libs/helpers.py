
from functools import wraps
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
