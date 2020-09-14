from django.db import models
#TODO  【理解】User 函数的使用
from django.contrib.auth.models import User


# Create your models here.

class Topic(models.Model):
    """用户学习的主题"""
    text = models.CharField(max_length=200)
    date_add = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE)
    def __str__(self):
        return self.text


class Entry(models.Model):
    """关于某个知识点的主题""" 
    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'entries'

    """显示前 50 条"""
    
    def __str__(self):
        return self.text[:50] + "..."

       

