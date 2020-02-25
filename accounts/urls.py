from django.urls import path

from accounts import views
from accounts.views import account_result, task_add, task_send_email_to_zhake

urlpatterns = [
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('result/',account_result,name='result'),
    path('celery/',task_add),
    path('send_email_to_zhake/',task_send_email_to_zhake)
]
