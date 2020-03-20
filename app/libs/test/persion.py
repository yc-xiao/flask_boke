import time
from threading import Lock
lock = Lock()

class Persion(object):
    def __init__(self):
        self.n = 0.1
        self.score = 0
        name = 'xiaom'

    def add(self, num):
        with lock:
            time.sleep(self.n)
            self.score += num
            time.sleep(self.n)

    def reduce(self, num):
        with lock:
            time.sleep(self.n)
            self.score -= num
            time.sleep(self.n)

    def test(self, num):
        for i in range(num):
            self.score += num
        for i in range(num):
            self.score -= num

    def testl(self, num):
        with lock:
            for i in range(num):
                self.score += num
            for i in range(num):
                self.score -= num

    @property
    def num(self):
        return self.score

    @num.setter
    def num(self, num):
        self.score += num
        self.score -= num

    @property
    def lnum(self):
        with lock:
            return self.score

    @lnum.setter
    def lnum(self, num):
        with lock:
            self.score += num
            time.sleep(self.n)
            self.score -= num

persion = Persion()
