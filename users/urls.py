from django.urls import path
from django.contrib.auth.views import LoginView
from . import views #从当前文件夹引入 views

urlpatterns = [
    #主页
    #Django 2.0 引入了 LoginView,Django2.0的内置登陆视图不再是函数，而是类，位置在django.contrib.auth.views.LoginView
    #参考文档 https://docs.djangoproject.com/zh-hans/3.1/topics/auth/
    path('login/', LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/', views.logout_view,name='logout'),
]
