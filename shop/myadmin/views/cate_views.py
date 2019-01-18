from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
from django.core.paginator import Paginator

def tab():
    cates = models.Cates.objects.extra(select = {'newpath':'concat(paths,id)'}).order_by('newpath')
    for i in cates:
        num = i.paths.count(',')-1
        i.newname=num*'|----'
    return cates    

def addcate(request):
    if request.method=='GET':
        # 将所有的类型返回
        cates = tab()

        return render(request,'myadmin/cate/addcate.html',{'cates':cates})
    elif request.method=='POST':
        # 接受pid 通过pid来判断是不是顶级分类
        pid = request.POST.get('pid')
        name = request.POST.get('name')
       
        if pid=='0':
            cate = models.Cates()
            cate.name=name
            cate.upid=int(pid)
            cate.paths='0,'
            cate.save()
        else:
            # 根据pid找父级 paths
            pobj = models.Cates.objects.get(id=pid)
            c = models.Cates()
            c.name=name
            c.upid=pobj.id
            c.paths=pobj.paths+pid+','
            c.save()
        cates = tab()  
            
        # 接受数据添加数据
        return render(request,'myadmin/cate/catelist.html',{'cates':cates})



def catelist(request):
    cates = tab()
    p=Paginator(cates,10)
    sumpage=p.num_pages
    page=int(request.GET.get('p',1))
    page1=p.page(page)
    if page<=3:
        prange=p.page_range[:5]
    elif page+2>=sumpage:
        prange=p.page_range[-5:]
    else:
        prange=p.page_range[page-3:page+2]
    
    return render(request,'myadmin/cate/catelist.html',{'cates':page1,'prange':prange,'page':page,'sumpage':sumpage})
  
    


def delcate(request):
    pid=int(request.GET.get('pid'))
    cnum=models.Cates.objects.filter(upid=pid).count()
    if cnum:
        return JsonResponse({'msg':0})
    else:
        c=models.Cates.objects.get(id=pid)
        c.delete()
        return JsonResponse({'msg':1})

def editcate(request):
    # 接受id和name
    cid = int(request.GET.get('id'))
    cname = request.GET.get('name')
    try:
        cate = models.Cates.objects.get(id=cid)
        cate.name=cname
        cate.save()
        return JsonResponse({'msg':1})
    except :
        return JsonResponse({'msg':0})
