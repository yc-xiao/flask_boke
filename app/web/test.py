from .base import web

@web.route('/test_error/')
def test_error():
    raise Exception('测试错误！！！')
