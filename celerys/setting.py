from datetime import timedelta
from celery.schedules import crontab

# "celery-task-meta-a2da068c-d37a-41be-b80a-e844baa4aae0"redis的keys
BROKER_URL = 'redis://localhost:6379' # 使用Redis作为消息代理(中间人)
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0' # 把任务结果存在了Redis
CELERY_TASK_SERIALIZER = 'pickle' # 任务序列化和反序列化使用msgpack方案
CELERY_RESULT_SERIALIZER = 'json' # 读取任务结果一般性能要求不高，所以使用了可读性更好的JSON
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24 # 任务过期时间
CELERY_ACCEPT_CONTENT = ['json', 'pickle'] # 指定接受的内容类型

CELERY_IMPORTS = (                          # 指定导入的任务模块
    'celerys.tasks.task_test',
    'celerys.tasks.task_send_email',
    'celerys.tasks.task_check_ip',
)

# Timezone
CELERY_TIMEZONE='Asia/Shanghai'    # 指定时区，不指定默认为 'UTC'

# schedules
CELERYBEAT_SCHEDULE = {
    'add-every-30-seconds': {
         'task': 'celerys.tasks.task_check_ip.check',
         'schedule': timedelta(seconds=3600),       # 每 30 秒执行一次
         'args': ()                           # 任务函数参数
    },
    # 'multiply-at-some-time': {
    #     'task': 'celery_app.task2.multiply',
    #     'schedule': crontab(hour=9, minute=50),   # 每天早上 9 点 50 分执行一次
    #     'args': (3, 7)                            # 任务函数参数
    # }
}
