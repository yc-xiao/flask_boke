from collections import defaultdict
from pprint import pprint
import time
import os

from main import app

PATH = r'/etc/nginx/black.ips'
error_ips = set()

def handler_error_addr(datas):
    global error_ips
    ip_urls = defaultdict(lambda: 0)
    for data in datas:
        data = data.split(' ')
        ip, url = data[1], data[3]
        for key in ['php', 'admin']:
            if key in url:
                ip_urls[ip] += 1
                continue
        if 'http' in url and '49.234.194.213' not in url:
            ip_urls[ip] += 5
    return ip_urls

def handler_error_status(datas):
    global error_ips
    ip_status = defaultdict(lambda: 0)
    for data in datas:
        data = data.split(' ')
        ip, status = data[1], data[5]
        if status.isdigit() and 400<= int(status) < 500:
            ip_status[ip] += 1
    return ip_status

def handler_error_user_agent(datas):
    global error_ips
    error_user_agents = ['masscan', 'Go-http-client', 'python', 'java']
    ip_user_agent = defaultdict(lambda: 0)
    for data in datas:
        data = data.split(' ')
        ip, user_agent = data[1], data[8]
        for error_user_agent in error_user_agents:
            if error_user_agent in user_agent:
                ip_user_agent[ip] += 2
                break
    return ip_user_agent


def handler(datas):
    global error_ips
    funcs = [handler_error_addr, handler_error_status, handler_error_user_agent]
    for func in funcs:
        error_ip_dic = func(datas)
        # pprint(error_ip_dic)
        for ip, count in error_ip_dic.items():
            if count > 2:
                error_ips.add(ip)
    with open(PATH) as f:
        datas = f.readlines()
        for data in datas:
            if not data:
                continue
            data = data[5:-2]
            error_ips.add(data)

    with open(PATH, 'w') as f:
        for ip in error_ips:
            f.write(f'deny {ip};\n')

@app.task
def check():
    now = time.strftime("%Y-%m-%d", time.localtime())
    path = f'/home/share/nginx/log/flask/{now}_access.log'
    size = os.path.getsize(PATH)
    with open(path) as f:
        datas = f.readlines()
    handler(datas)
    size2 = os.path.getsize(PATH)
    if size != size2:
        os.system("nginx -s reload")


def main():
    now = time.strftime("%Y-%m-%d", time.localtime())
    path = f'/home/share/nginx/log/flask/{now}_access.log'
    # path = f'{now}_access.log'
    while True:
        size = os.path.getsize(PATH)
        with open(path) as f:
            datas = f.readlines()
        handler(datas)
        size2 = os.path.getsize(PATH)
        if size != size2:
            os.system("nginx -s reload")
        break
        time.sleep(TIME)

if __name__ == '__main__':
    main()
