from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
from . import cate_views,user_views
import os
from django.core.paginator import Paginator

def addgoods(request):
    types=cate_views.tab()
    return render(request,'myadmin/goods/addgoods.html',{'types':types})



def goodslist(request):
    goods = models.Goods.objects.all()

    types = request.GET.get('type')
    # 接受关键字
    search = request.GET.get('search')
    # 判断用是否搜索内容
    if types:
        if types=='all':
            #根据id username phone
            # select * from myadmin_users where id like %search% or username like %search% or phone like %search%
            from django.db.models import Q

            goods = models.Goods.objects.filter(Q(id__contains=search)|Q(title__contains=search)|Q(price__contains=search)|Q(ordernum__contains=search))
        elif types=='title':
            goods = models.Goods.objects.filter(title__contains=search)
        elif types=='price':
            goods = models.Goods.objects.filter(price__contains=search)
        elif types == 'ordernum':
            goods = models.Goods.objects.filter(ordernum__contains=search)
        

    p=Paginator(goods,3)
    sumpage=p.num_pages
    page=int(request.GET.get('p',1))
    page1=p.page(page)
    if page<=3:
        prange=p.page_range[:5]
    elif page+2>=sumpage:
        prange=p.page_range[-5:]
    else:
        prange=p.page_range[page-3:page+2]

    return render(request,'myadmin/goods/list.html',{'goods':page1,'prange':prange,'page':page,'sumpage':sumpage})

    


def goodsinsert(request):
    ginfo = request.POST.dict()
    ginfo.pop('csrfmiddlewaretoken')
    print(ginfo)

    file = request.FILES.get('g_url')
    if not file:
        return HttpResponse('<script>alert("请选择图片");history.back(-1)</script>')


    # 调图片上传
    g_url=user_views.upload(file)

    # 入库
    goods = models.Goods()
    goods.title=ginfo['title']
    goods.ordernum=ginfo['ordernum']
    goods.g_url=g_url
    goods.price=ginfo['price']
    goods.ginfo=ginfo['ginfo']
    goods.cateid=models.Cates.objects.get(id=ginfo['cateid'])
    goods.save()

    # 返回
    return redirect(reverse('myadmin_goodslist'))


def delgoods(request):
    uid=request.GET.get('uid')
    goods=models.Goods.objects.get(id=uid)
    goods.delete()
    
    return redirect(reverse('myadmin_goodslist'))


def editgoods(request):
    types=cate_views.tab()
    uid=request.GET.get('uid')
    if request.method=='GET':
        goods=models.Goods.objects.get(id=uid)
        return render(request,'myadmin/goods/edit.html',{'goods':goods,'types':types})
    elif request.method=='POST':
        cinfo = request.POST.dict()
        goodsinfo=models.Goods.objects.get(id=uid)
        goodsinfo.title=cinfo['title']
        goodsinfo.price=cinfo['price']
        goodsinfo.ordernum=cinfo['ordernum']
        goodsinfo.ginfo=cinfo['ginfo']
        

        file=request.FILES.get('g_url')
        if file:
            os.remove('.'+goodsinfo.g_url)
            headurl=user_views.upload(file)
            goodsinfo.g_url=headurl

        goodsinfo.save()
        return redirect(reverse('myadmin_goodslist'))