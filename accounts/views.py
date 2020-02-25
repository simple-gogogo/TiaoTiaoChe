import logging

from django.contrib.auth import get_user_model, REDIRECT_FIELD_NAME
from django.contrib.auth.forms import AuthenticationForm
from django.db.transaction import atomic
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import FormView

from tiaotiaoche import settings
from accounts.forms import RegisterForm, LoginForm
from utils import get_current_site, get_md5, send_email

logger = logging.getLogger(__name__)

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'account/registration_form.html'

    def form_valid(self, form):
        if form.is_valid():
            with atomic():
                user = form.save(False)
                user.is_active = False
                user.source = 'Register'
                user.save(True)
                site = get_current_site().domain
                sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))

                if settings.DEBUG:
                    site = '127.0.0.1:8000'
                path = reverse('account:result')
                url = "http://{site}{path}?type=validation&id={id}&sign={sign}".format(site=site, path=path, id=user.id,
                                                                                       sign=sign)

                content = """
                                <p>请点击下面链接验证您的邮箱</p>
    
                                <a href="{url}" rel="bookmark">{url}</a>
    
                                再次感谢您！
                                <br />
                                如果上面链接无法打开，请将此链接复制至浏览器。
                                {url}
                                """.format(url=url)
                send_email(emailto=[user.email, ], title='验证您的电子邮箱', content=content)

                url = reverse('account:result') + '?type=register&id=' + str(user.id)
                return HttpResponseRedirect(url)
        else:
            return self.render_to_response({
                'form': form
            })


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        kwargs['redirect_to'] = redirect_to
        return super(LoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        form = AuthenticationForm(data=self.request.POST, request=self.request)
        if form.is_valid():
            pass
        return self.render_to_response({'form': form})


def account_result(request):
    type = request.GET.get('type')
    id = request.GET.get('id')
    user = get_object_or_404(get_user_model(), id=id)
    logger.info(type)
    if user.is_active:
        return HttpResponseRedirect('/')
    if type and type in ['register', 'validation']:
        if type == 'register':
            content = '''
    恭喜您注册成功，一封验证邮件已经发送到您 {email} 的邮箱，请验证您的邮箱后登录本站。
    '''.format(email=user.email)
            title = '注册成功'
        else:
            c_sign = get_md5(get_md5(settings.SECRET_KEY + str(user.id)))
            sign = request.GET.get('sign')
            if sign != c_sign:
                return HttpResponseForbidden()
            user.is_active = True
            user.save()
            content = '''
            恭喜您已经成功的完成邮箱验证，您现在可以使用您的账号来登录本站。
            '''
            title = '验证成功'
        return render(request, 'account/result.html', {
            'title': title,
            'content': content
        })
    else:
        return HttpResponseRedirect('/')

from django.http import HttpResponse

from accounts.tasks import add,send_email_to_zhake

def task_add(request):
    # delay() 方法调用任务
    # delay 返回的是一个 AsyncResult 对象，里面存的就是一个异步的结果，
    # 当任务完成时result.ready() 为 true，然后用 result.get() 取结果即可

    # 发出request后异步执行该task, 马上返回response, 从而不阻塞该request,
    # 使用户有一个流畅的访问过程.那么, 我们可以使用.delay,
    add.delay(3, 5)
    # Celery会将task加入到queue中, 并马上返回.而在一旁待命的worker看到该task后, 便会按照设定执行它, 并将他从queue中移除
    return HttpResponse("假装操作很耗时，不等了")

def task_send_email_to_zhake(request):
    send_email_to_zhake.delay()
    return HttpResponse("假装发送失败")
