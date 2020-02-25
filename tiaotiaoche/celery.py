from __future__ import absolute_import

import os

from celery import Celery,platforms
from django.conf import settings
# 设置环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiaotiaoche.settings')
# 实例化Celery
app = Celery('task')
# 使用django的settings文件配置celery
app.config_from_object('django.conf.settings')
# Celery加载所有注册的应用
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

