from celerys.main import appc

@appc.task
def add(x,y):
    return x+y
