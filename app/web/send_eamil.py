from celerys.tasks.task_send_email import send_email
from .base import web

@web.route('/send/<string:email>')
def send(email):
    send_email.delay(to_addr=email)
    return 'ok'
