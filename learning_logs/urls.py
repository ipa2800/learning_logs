#定义 Learning_logs 的 URL 模式
from django.urls import path
from . import views #从当前文件夹引入 views

urlpatterns = [
    #主页
    path('',views.index, name="index"),
    path('topics/',views.topics, name="topics"),
    path('topics/<int:topic_id>/',views.topic,name="topic"),
    path('new_topic/',views.new_topic,name='new_topic'),
    path('new_entry/<int:topic_id>/',views.new_entry,name='new_entry'),
    path('edit_entry/<int:entry_id>/',views.edit_entry,name='edit_entry'),
]
