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


class Goods(models.Model):
    # id titlt order_num status price img clicknum addtime 
    title = models.CharField(max_length=100)
    g_url = models.CharField(max_length=200)
    price = models.IntegerField()
    ordernum = models.IntegerField()
    ginfo = models.TextField()

    status = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    cateid=models.ForeignKey(to="Cates",to_field="id")




class Car(models.Model):
    # id gid num uid
    gid=models.ForeignKey(to="Goods",to_field="id")
    num = models.IntegerField()
    uid=models.ForeignKey(to="Users",to_field="id")