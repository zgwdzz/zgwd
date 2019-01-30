from django.shortcuts import render,redirect
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

# 购物车页面
def carpage(request):
    uid=request.session.get('userinfo')
    if not uid:
        return HttpResponse('<script>alert("没有登录");location.href="'+reverse('myhome_login')+'"</script>')
    user=models.Users.objects.get(id=uid['uid'])
    cgoods=user.car_set.all()
    return render(request,'myhome/cart.html',{'cgoods':cgoods})



    

# 修改数量
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
   
    return JsonResponse({'msg':'删除成功'})


# 确认订单页
def confirm(request):
    # 接受购物车的id
    cart = request.GET.get('cid').split(',')
    cargoods = models.Car.objects.filter(id__in=cart)

    # 返回一级城市的数据
    citys = models.Citys.objects.filter(upid=0)

    # 当前用户的收货地址
    userobj = models.Users.objects.get(id=request.session['userinfo']['uid'])
    address = userobj.address_set.all()
    print(address)

    return render(request,'myhome/pay.html',{'cargoods':cargoods,'citys':citys,'address':address})

# 城际联动
def getcitys(request):
    # 接受upid
    upid = request.GET['upid']
    citys = models.Citys.objects.filter(upid=upid).values()
    return JsonResponse(list(citys),safe=False)
# 存地址
def saveaddress(request):
    # 接受
    addinfo = request.GET.dict()
    # 存数据
    address = models.Address()
    address.uid = models.Users.objects.get(id=request.session['userinfo']['uid'])
    addnum=models.Address.objects.filter(uid=request.session['userinfo']['uid']).count()
    print(addnum,11111111111111111111111111111111)
    if addnum == 0:
        address.isselect = 1
    else:
        address.isselect = 0

    address.name=addinfo['name']
    address.phone=addinfo['phone']
    address.sheng=models.Citys.objects.get(id=addinfo['sheng']).name
    address.shi=models.Citys.objects.get(id=addinfo['shi']).name
    address.xian=models.Citys.objects.get(id=addinfo['xian']).name
    address.addinfo=addinfo['addinfo']
    
    address.save()
    return JsonResponse({'error':0,'msg':'添加成功'})

# 生成订单
def createorder(request):
    oinfo = request.POST.dict()
    # 订单
    order = models.Order()
    order.uid = models.Users.objects.get(id = request.session['userinfo']['uid'])
    order.phone = models.Address.objects.get(id=oinfo['dizhi']).phone
    order.name = models.Address.objects.get(id=oinfo['dizhi']).name
    # 地址
    sheng = models.Address.objects.get(id=oinfo['dizhi']).sheng
    shi = models.Address.objects.get(id=oinfo['dizhi']).shi
    xian = models.Address.objects.get(id=oinfo['dizhi']).xian
    addinfo = models.Address.objects.get(id=oinfo['dizhi']).addinfo
    order.addinfo = sheng+shi+xian+addinfo

    order.wl = int(oinfo['wuliu'])
    order.pay = int(oinfo['zhifu'])

    order.total=0
    order.save()

    
    total=0
    carts = models.Car.objects.filter(id__in=oinfo['car'].split(','))
    for i in carts:
        # 订单详情
        orderinfo = models.Orderinfo()
        orderinfo.orderid = order
        orderinfo.num = i.num
        orderinfo.price = i.gid.price
        orderinfo.gid = i.gid
        orderinfo.save()
        total += i.num*i.gid.price
        i.delete()
        

    order.total = total
    order.save()



    return HttpResponse('<script>alert("提交成功,请去个人中心订单管理页面支付");location.href="'+reverse('myhome_order')+'"</script>')