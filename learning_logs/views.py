from django.shortcuts import render
from .models import Topic,Entry
#redirect 模块用于用户提交数据后重定向
from django.http import HttpResponseRedirect
#reverse 函数，根据指定的 URL 模型生成 URL
from django.urls import reverse
from .forms import TopicForm,EntryForm

# Create your views here.

def index(request):
    # 学习笔记的主页
    return render(request,'learning_logs/index.html')

def topics(request):
    # 显示所有的主题
    topics = Topic.objects.order_by('date_add')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html',context)

def topic(request,topic_id):
    # 显示主题详情
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    # 返回一个字典给模板用，还是挺方便的
    return render(request,'learning_logs/topic.html',context)

def new_topic(request):
    # 添加新主题
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    
    else:
        # POST 提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic'))
    
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html', context)

# 如何定义新条目，完全还没有搞懂
    
def new_entry(request,topic_id):
    # 在主题下添加新条目

    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = EntryForm()
    
    else:
        # POST 提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic_id]))
    
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html', context)

def edit_entry(request,entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
    context = {'entry': entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)

