from email.message import EmailMessage
import smtplib

from celerys.main import appc
from app.secure import EMAIL_ACCOUNT, EMAIL_PASSWORD

@appc.task
def send_email(subject='pytest', to_addr=None, content=None):
    if not to_addr:
        return
    smtp_server = 'smtp.qq.com'    # 定义SMTP服务器地址:
    from_addr = EMAIL_ACCOUNT # 定义发件人地址
    password = EMAIL_PASSWORD  # 定义登录邮箱的密码
    to_addr = to_addr   # 定义收件人地址:
    conn = smtplib.SMTP_SSL(smtp_server, 465)  # 创建SMTP连接
    conn.login(from_addr, password)
    # 创建邮件对象
    msg = EmailMessage()
    msg['subject'] = subject
    msg['from'] = '小明 <%s>' % from_addr
    msg['to'] = '新用户 <%s>' % to_addr
    content = '您好，这是一封来自Python的邮件' if not content else content
    msg.set_content(content, 'plain', 'utf-8') # 设置邮件内容
    conn.sendmail(from_addr, [to_addr], msg.as_string()) # 发送邮件
    conn.quit() # 退出连接
