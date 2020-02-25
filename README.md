# 跳跳二手车交易网
#### 项目简介

该项目是一个使用Django2开发的一个二手车交易平台，免费发布全国二手车出售、转让信息，专业整合二手车行业资源为买卖双方提供及时的交易信息服务.

#### 开发环境

​	·  操作系统: unbuntu18.04

​	·  Python版本: 3.6.5

​	·  集成开发工具: Pycharm

#### 推荐书单与学习网站

​	·  Django官方文档

​	·  Django Github源码

### Django在项目中的实战
#### 相关用法汇总
##### 1.DRF定制数据接口

##### 什么是restful?

REST是所有Web应用都应该遵守的架构设计指导原则。

Representational State Transfer，翻译是”表现层状态转化”。

REST核心: **资源， 状态转移， 统一接口**

**资源:** 是REST最明显的特征,是指对某类信息实体的抽象，资源是服务器上一个可命名的抽象概念，资源是以名词为核心来组织的，首先关注的是名词。

**状态转移:** 是指客户端痛服务端进行交互的过程中，客户端能够通过对资源的表述，实现操作资源的目的

**统一接口:** REST要求，必须通过统一的接口来对资源执行各种操作。对于每个资源只能执行一组有限的操作。 比如，客户端通过HTTP的4个请求方式(POST, GET, PUT, PATCH)来操作资源，也就意味着不管你的url是什么，不管请求的资源是什么但操作的资源接口都是统一的。

GET用来获取资源，POST用来新建资源（也可以用于更新资源），PUT(PATCH)用来更新资源，DELETE用来删除资源。

使用目的：提供前后端分离的架构模式。 

1.提供了定义序列化器Serializer的方法,可以快速根据Django ORM 或者其他库自动序列化/反序列化
2.提供了丰富的类视图扩展类,简化视图的编写
3.丰富的定制层级:函数视图\类视图\结合到自动生成API,满足各种需要
4.多种身份认证和权限认证方式的支持
5.直观的API web界面


##### 安装

```python
pip install djangorestframework
pip install markdown       
pip install django-filter  
```

创建django超级用户

```python
python manage.py createsuperuser --email admin@163.com --username admin
```

Django 项目 settings.py修改

```python
INSTALLED_APPS = (
    ...
    'rest_framework',
)
```

```
urlpatterns = [
    ...
    url(r'^api/', include('rest_framework.urls'))
]
```

##### 2. Celery异步执行消息推送

celery是一个基于python开发的简单、灵活且可靠的分布式任务队列框架，支持使用任务队列的方式在分布式的机器/进程/线程上执行任务调度。采用典型的生产者-消费者模型，主要由三部分组成：

1. 消息队列broker：broker实际上就是一个MQ队列服务，可以使用Redis、RabbitMQ等作为broker
2. 处理任务的消费者workers：broker通知worker队列中有任务，worker去队列中取出任务执行，每一个worker就是一个进程
3. 存储结果的backend：执行结果存储在backend，默认也会存储在broker使用的MQ队列服务中，也可以单独配置用何种服务做backend

##### 使用
安装celery

```shell
# pip install celery -i https://pypi.douban.com/simple
```

3.celery用在django项目中，django项目目录结构(简化)如下

```
tiaotiaoche/
|-- accounts
|   |-- admin.py
|   |-- apps.py
|   |-- __init__.py
|   |-- models.py
|   |-- tasks.py
|   |-- tests.py
|   |-- urls.py
|   `-- views.py
|-- manage.py
|-- README
`-- tiaotiaoche
    |-- celery.py
    |-- __init__.py
    |-- settings.py
    |-- urls.py
    `-- wsgi.py
```

4.创建`tiaotiaoche/celery.py`主文件

```python
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tiaotiaoche.settings')

app = Celery('tiaotiaoche')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

5.在`tiaotiaoche/__init__.py`文件中增加如下内容，确保django启动的时候这个app能够被加载到

```python
from __future__ import absolute_import

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ['celery_app']
```

6.各应用创建tasks.py文件，这里为`accounts/tasks.py`

```python
from __future__ import absolute_import
from celery import shared_task
from users.models import *
from tiaotiaoche.celery import app

@app.task
def add(x, y):
    # 模拟长时间耗时操作
    print('============耗时操作=============')
    time.sleep(10)
    print('============耗时操作结束============')
    return x + y
```

- **注意tasks.py必须建在各app的根目录下，且只能叫tasks.py，不能随意命名**

7.views.py中引用使用这个tasks异步处理

```python
from accounts.tasks import add

def add_some(request):
    add.delay()
    result_json = {}
    return JsonResponse(result_json, safe=False)
```

- 使用函数名.delay()即可使函数异步执行
- 可以通过`result.ready()`来判断任务是否完成处理
- 如果任务抛出一个异常，使用`result.get(timeout=1)`可以重新抛出异常
- 如果任务抛出一个异常，使用`result.traceback`可以获取原始的回溯信息

8.启动celery

```shell
# celery -A tiaotiaoche worker -l info
```

9.这样在调用post这个方法时，里边的add就可以异步处理了



### 未完待续.........


