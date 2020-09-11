from django import forms
from .models import Topic,Entry

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']
        labels = {'text': ''}

class EntryForm(forms.ModelForm):  
    class Meta:
        model = Entry
        fields = ['text']
        # 给 text 定义了一个空标签
        labels = {'text': ''}
        # widget 定义了表单元素，设置文本框的输入宽度
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}


