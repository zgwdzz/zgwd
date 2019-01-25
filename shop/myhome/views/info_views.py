from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from myadmin import models
from django.core.urlresolvers import reverse
# Create your views here.
def myhome_info(request):
    gid =request.GET.get('gid')
    gobj = models.Goods.objects.get(id=gid)

    return render(request,'myhome/goodsinfo.html',{'ginfo':gobj})



def addcar(request):
    try:
        info =request.GET.dict()
        gobj=models.Goods.objects.get(id=info['gid'])
        uobj=models.Users.objects.get(id=request.session['userinfo']['uid'])
        flag=models.Car.objects.filter(uid=uobj.id).filter(gid=gobj.id)
        if flag.count():
            for i in flag:
                i.num+=int(info['num'])
                i.save()
        else:
            car=models.Car()
            car.num=int(info['num'])
            car.gid=gobj
            car.uid=uobj
            car.save()
        return JsonResponse({"msg":1,'info':'添加成功'})
    except :
        return JsonResponse({"msg":1,'info':'添加失败'})   


    return HttpResponse('ok') 


def carpage(request):
    uid=request.session.get('userinfo')
    if not uid:
        return HttpResponse('<script>alert("没有登录");location.href="'+reverse('myhome_login')+'"</script>')
    user=models.Users.objects.get(id=uid['uid'])
    cgoods=user.car_set.all()
    return render(request,'myhome/cart.html',{'cgoods':cgoods})



    


def caredit(request):
    cinfo=request.GET.dict()
    cobj=models.Car.objects.get(id=cinfo['cid'])
    cobj.num=int(cinfo['num'])
    cobj.save()
    return JsonResponse({'error':1,'msg':'修改成功'})



def delcar(request):
    cinfo=request.GET.dict()
    print(cinfo)
    cobj=models.Car.objects.get(id=cinfo['cid'])
    # print(cobj)
    cobj.delete()
   
    return JsonResponse({'msg':'修改成功'})

   