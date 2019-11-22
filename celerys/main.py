from celery import Celery

app = Celery('flask_celery')
app.config_from_object('setting')

if __name__ == '__main__':
    app.start()
