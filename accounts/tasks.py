import time

import django
django.setup()

#调度任务
from celery import shared_task
from celery.task import periodic_task

from tiaotiaoche.celery import app
from utils import send_email


@app.task
def add(x, y):
    # 模拟长时间耗时操作
    print('============耗时操作=============')
    time.sleep(10)
    print('============耗时操作结束============')
    return x + y



@shared_task
def send_email_to_zhake():
    content = """
                    <p>这是给扎克的第一封邮件</p>
                    <p>嘿嘿！！！</p>
                    """
    print('============发送中=============')
    send_email(emailto=['1092389493@qq.com', ], title='猴急', content=content)
    print('============完毕=============')
