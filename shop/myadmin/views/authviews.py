from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,Permission,Group
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse


def permission_denied(request):
    return render(request, '403.html')



def mylogin(request):
    if request.method=='GET':
        return render(request,'myadmin/login.html')
    elif request.method=='POST':
        user=request.POST.dict()
        
        if user['yzm'].upper() != request.session['verifycode'].upper():
            return HttpResponse('<script>alert("验证码错误，重新输入");location.href="'+reverse('myadmin_login')+'"</script>')
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return HttpResponse('<script>alert("登录成功");location.href="/myadmin/"</script>')

        
        return HttpResponse('<script>alert("用户名或密码错误");location.href="/myadmin/login/"</script>')


def outlogin(request):
    logout(request)
    # 跳转到登录页面
    return HttpResponse('<script>alert("退出成功");location.href="'+reverse('myadmin_login')+'"</script>')  

def userdel(request,uid):
    ob=User.objects.get(id=uid)
    ob.delete()
    return HttpResponse('<script>location.href="/myadmin/auth/user/list"</script>')



# 管理员用户
def useradd(request):
    if request.method == 'GET':

        glist=Group.objects.all()
        context={'glist':glist}
        return render(request,'auth/user/add.html',context)
    elif request.method == 'POST':
       # 判断是超级还是普通
        if request.POST['is_superuser'] == '1':
            ob = User.objects.create_superuser(request.POST['username'],request.POST['email'],request.POST['password'])
            
        else:
            ob = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])
        ob.save()

        gs=request.POST.getlist('gs',None)
        if gs:
            ob.groups.set(gs)
            ob.save()


    return HttpResponse('<script>location.href="/myadmin/auth/user/list/"</script>')



def userlist(request):
    data = User.objects.all()
    context={'ulist':data}

    return render(request,'auth/user/list.html',context)



def groupadd(request):
    if request.method == 'GET':
        perms = Permission.objects.exclude(name__istartswith='Can')
        context = {'perms':perms}
        return render(request,'auth/group/add.html',context)
    elif request.method == 'POST':
        g=Group(name=request.POST['name'])
        g.save()
        prms=request.POST.getlist('prms',None)
        if prms:
            g.permissions.set(prms)
            g.save()


        return HttpResponse('<script>location.href="/myadmin/auth/group/list/"</script>')


def grouplist(request):

    data=Group.objects.all()
    context={'glist':data}
    return render(request,'auth/group/list.html/',context)

def groupedit(request,gid):
    ginfo = Group.objects.get(id=gid)
    if request.method == 'GET':
        
        perms = Permission.objects.exclude(name__istartswith='Can').exclude(group=ginfo)
        context={'ginfo':ginfo,'perms':perms}

        return render(request,'auth/group/edit.html',context)

    elif request.method == 'POST':
        ginfo.name = request.POST['name']
        prms=request.POST.getlist('prms',None)

        ginfo.permissions.clear()


        if prms:
             ginfo.permissions.set(prms)
        ginfo.save()
        return HttpResponse('<script>location.href="/myadmin/auth/group/list/"</script>')
        


def verifycode(request):
    #引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), 255)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 200):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象
    font = ImageFont.truetype('FreeMono.ttf', 23)
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
