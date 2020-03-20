from app.libs.test.persion import persion
from .base import web

import threading

# ab -n 请求总数　-c 并发量

@web.route('/test_thread/test/<int:num>')
def test_xpersion(num):
    persion.test(num)
    if persion.num != 0:
        print(persion.num)
    return str(persion.num)

@web.route('/test_thread/testl/<int:num>')
def test_xlpersion(num):
    # ab -n 100 -c 10 http://127.0.0.1:5000/test_thread/testl/100000
    persion.testl(num) # 加锁后保证testl原子性,但是persion的其他方法非原子性，且各个方法直接互不影响
    if persion.num != 0:
        print(persion.num)
    return str(persion.num)


@web.route('/test_thread/post/<int:num>')
def test_persion(num):
    persion.num = num
    if persion.num != 0:
        print(persion.num)
    return str(persion.num)

@web.route('/test_thread/post/lock/<int:num>')
def test_lpersion(num):
    # ab -n 10000 -c 1000 http://127.0.0.1:5000/test_thread/post/lock/100
    # ab 测试一万条请求，　1000个并发
    persion.lnum = num # 保证原子性
    if persion.lnum != 0:
        print(persion.lnum)
    return str(persion.lnum)

@web.route('/test_thread/get/')
def test_persion_value():
    return str(persion.num)

@web.route('/test_thread/getl/')
def test_lpersion_value():
    return str(persion.lnum)
