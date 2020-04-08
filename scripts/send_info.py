from celerys.tasks.task_send_email import send_email
from random import randint
import requests
import json

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
client = AcsClient('', '', 'cn-hangzhou')

def send_phone_code(phone_number, code):
    data = {
        'phone_number': phone_number,
        'sign_name': '小明博客园',
        'template_code': 'SMS_186940119',
        'template_param': {
            'code': code
        }
    }
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('PhoneNumbers', data['phone_number'])
    request.add_query_param('SignName', data['sign_name'])
    request.add_query_param('TemplateCode', data['template_code'])
    request.add_query_param('TemplateParam', data['template_param'])

    response = client.do_action(request)
    response = json.loads(response)
    return response['Code']

def get_weather_forecast():
    gcity_id = '101280101'
    scity_id = '101280601'
    setting = {
        'appid': '84573994',
        'appsecret': 'WXeeXd3Q',
        'version': 'v61',
        'cityid': gcity_id
    }
    url = 'https://tianqiapi.com/api/?appid={appid}&appsecret={appsecret}&version={version}&cityid={cityid}'.format(**setting)
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        wea = data['wea']
        win = data['win']
        tem1 = data['tem1']
        return f"{data['aqi']['city']}今天天气 {data['wea']}，吹的{data['win']}。温度在 {data['tem2']}-{data['tem1']}，{data['air_tips']} 适合请客吃饭。"
    return '今天天气不好!!!'

def send_email_func(email):
    content = get_weather_forecast()
    data = {subject='good good study', to_addr=email, content=content}
    send_email(**data)

def send_phone_func(phone_number):
    send_phone_code(phone_number, randint(10000, 100000))

def main():
    phone_number, email = '', ''
    send_email_func(email)
    send_phone_func(phone_number)

if __name__ == '__main__':
    main()
