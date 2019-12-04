from celery import Celery, platforms

appc = Celery('flask_celery')
appc.config_from_object('celerys.setting')
platforms.C_FORCE_ROOT = True

if __name__ == '__main__':
    appc.start()
