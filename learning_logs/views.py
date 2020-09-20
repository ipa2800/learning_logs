from django.shortcuts import render
from .models import Topic,Entry
#redirect 模块用于用户提交数据后重定向
from django.http import HttpResponseRedirect,Http404
#reverse 函数，根据指定的 URL 模型生成 URL
from django.urls import reverse
from .forms import TopicForm,EntryForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    # 学习笔记的主页
    return render(request,'learning_logs/index.html')

#添加装饰器，限制只允许登录用户请求 topics 页面，login_required() 的代码检查用户是否已登录，仅当用户已登录时，Django才运行topics() 的代码。如果用户未登录，就重定向到登录页面。
@login_required
def topics(request):
    # 显示所有的主题
    topics = Topic.objects.filter(owner=request.user).order_by('date_add')
    context = {'topics':topics}
    return render(request, 'learning_logs/topics.html',context)

@login_required
def topic(request,topic_id):
    # 显示主题详情
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'topic':topic,'entries':entries}
    # 返回一个字典给模板用，还是挺方便的
    return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
    # 添加新主题
    if request.method != 'POST':
        # 未提交数据，创建一个新表单
        form = TopicForm()
    else:
        # POST 提交的数据，对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse('learning_logs:topics'))
    
    context = {'form':form}
    return render(request,'learning_logs/new_topic.html', context)

# TODO 动手试一试 19-3 重构 ：在views.py中，我们在两个地方核实主题关联到的用户为当前登录的用户。请将执行这种检查的代码放在一个名为check_topic_owner() 的函数中， 并在恰当的地方调用这个函数。 19-4 保护页面 new_entry ：一个用户可在另一个用户的学习笔记中添加条目，方法是输入这样的URL，即其中包含输入另一个用户的主题的ID。为防范这种攻击， 请在保存新条目前，核实它所属的主题归当前用户所有。 19-5 受保护的博客 ：在你创建的项目Blog中，确保每篇博文都与特定用户相关联。确保任何用户都可访问所有的博文，但只有已登录的用户能够发表博文以及编辑既 有博文。在让用户能够编辑其博文的视图中，在处理表单前确认用户编辑的是他自己发表的博文。


# 如何定义新条目，完全还没有搞懂

@login_required    
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
            return HttpResponseRedirect(reverse('learning_logs:topic',args= [topic_id]))
    
    context = {'topic':topic,'form':form}
    return render(request,'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request,entry_id):

    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry,data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic',args=[topic.id]))
    context = {'entry': entry,'topic':topic,'form':form}
    return render(request,'learning_logs/edit_entry.html',context)

