from celery import Celery

appc = Celery('flask_celery')
appc.config_from_object('celerys.setting')

if __name__ == '__main__':
    appc.start()
