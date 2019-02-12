from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from .. import models
import time,os
from django.core.paginator import Paginator
from django.contrib.auth.decorators import permission_required

@permission_required('myadmin.show_users', raise_exception = True)
def vipuser(request):
    userinfo=models.Users.objects.all().exclude(status=3)
    
    types = request.GET.get('type')
    # 接受关键字
    search = request.GET.get('search')
    # 判断用是否搜索内容
    if types:
        if types=='all':
            #根据id username phone
            # select * from myadmin_users where id like %search% or username like %search% or phone like %search%
            from django.db.models import Q

            userinfo = models.Users.objects.filter(Q(id__contains=search)|Q(username__contains=search)|Q(phone__contains=search))
        elif types=='uname':
            userinfo = models.Users.objects.filter(username__contains=search)
        elif types=='uphone':
            userinfo = models.Users.objects.filter(phone__contains=search)
        elif types == 'uid':
            userinfo = models.Users.objects.filter(id__contains=search)


    # 分页
    p=Paginator(userinfo,10)
    sumpage=p.num_pages
    page=int(request.GET.get('p',1))
    page1=p.page(page)
    if page<=3:
        prange=p.page_range[:5]
    elif page+2>=sumpage:
        prange=p.page_range[-5:]
    else:
        prange=p.page_range[page-3:page+2]
    
    return render(request,'myadmin/table-list.html',{'userinfo':page1,'prange':prange,'page':page,'sumpage':sumpage})
  




@permission_required('myadmin.insert_users', raise_exception = True)
def adduser(request):
    if request.method=='GET':
        return render(request,'myadmin/adduser.html')
    elif request.method=='POST':
        userinfo = request.POST.dict()
        userinfo.pop('csrfmiddlewaretoken')

        myfile=request.FILES.get("head_url",None)

        if not myfile:
                return HttpResponse("<script>alert('请选择头像');location.href=''</script>")
        userinfo['head_url']=upload(myfile)
        print(userinfo['head_url'],"111111")
        userinfo['password'] = make_password(userinfo['password'], None, 'pbkdf2_sha256')
       
        try:
            user=models.Users(**userinfo)
            user.save()
            return redirect(reverse('myadmin_vipuser'))

        except:
            return HttpResponse("<script>alert('添加失败！');location.href=''</script>")





@permission_required('myadmin.del_users', raise_exception = True)
def deluser(request):
    uid=request.GET.get('uid')
    user=models.Users.objects.get(id=uid)
    user.status=3
    user.save()
    return redirect(reverse('myadmin_vipuser'))


@permission_required('myadmin.edit_users' ,raise_exception = True)
def edituser(request):
    uid=request.GET.get('uid')
    if request.method=='GET':
        user=models.Users.objects.get(id=uid)
        return render(request,'myadmin/edit.html',{'user':user})
    elif request.method=='POST':
        userinfo = request.POST.dict()
        uinfo=models.Users.objects.get(id=uid)
        uinfo.username=userinfo['username']
        uinfo.phone=userinfo['phone']
        uinfo.age=userinfo['age']
        uinfo.sex=userinfo['sex']

        file=request.FILES.get('head_url')
        if file:
            os.remove('.'+uinfo.head_url)
            headurl=upload(file)
            uinfo.head_url=headurl

        uinfo.save()
        return redirect(reverse('myadmin_vipuser'))
    
    








# 封装的头像上传函数
def upload(myfile):
    filename=str(time.time())+"."+myfile.name.split('.').pop()
    destination=open("./static/pics/"+filename,"wb+")
    for chunk in myfile.chunks():
        destination.write(chunk)
    destination.close()
    return '/static/pics/'+filename

# 重置密码
def respwd(request):
    uid=request.GET.get('uid')
    user=models.Users.objects.get(id=uid)
    user.password=make_password('123456',None, 'pbkdf2_sha256')
    user.save()
    data={'msg':'密码重置为123456'}
    return JsonResponse(data)

# 改变状态
def changes(request):
    uid=request.GET.get('uid')
    status=request.GET.get('status')

    try:
        user=models.Users.objects.get(id=uid)
        user.status=int(status)
        user.save()
        msg={'msg':'修改成功'}
        return JsonResponse(msg)
    except:
        msg={'msg':'修改失败'}
        return JsonResponse(msg)