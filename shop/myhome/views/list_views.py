from django.shortcuts import render
from django.http import HttpResponse
from myadmin import models
# Create your views here.
def myhome_list(request,cid,bid):
    ob1=models.Cates.objects.get(id=cid)
    ob2=models.Cates.objects.filter(upid=cid)
    goods=[]
    bid=int(bid)
    for cate2 in ob2:
        if cate2.id !=bid and bid !=0:
            continue
        goods.append(cate2.goods_set.all())




    content={'cate1':ob1,'cate2':ob2,'goods':goods,'color':bid}

    return render(request,'myhome/list.html',content)