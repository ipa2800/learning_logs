from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('learning_logs:index'))

def register(request): 

    if request.method != 'POST':
        #UserCreationForm 这里调用了Django 的默认表单，因此会有对应的处理方法
        form = UserCreationForm()
    else:
        form = UserCreationForm(data=request.POST)
    
        if form.is_valid():
            new_user = form.save()
            #passowrd1 是获取表单中经一致性校验的第一个，作为密码
            authenticated_user = authenticate(username=new_user.username,password=request.POST['password1'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form':form}
    return render(request,'users/register.html',context)

    

