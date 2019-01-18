from django.db import models

# Create your models here.
class Users(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=100)
    phone=models.CharField(max_length=11)
    sex=models.CharField(max_length=1)   
    age=models.CharField(max_length=3)   
    head_url=models.CharField(max_length=100) 

    status=models.IntegerField(default=0)   
    addtime=models.DateTimeField(auto_now_add=True)  


class Cates(models.Model):
    name=models.CharField(max_length=50)
    upid=models.IntegerField()
    paths=models.CharField(max_length=50)
