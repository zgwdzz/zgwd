from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User,Permission,Group


# 管理员用户
def useradd(request):
    if request.method == 'GET':
        return render(request,'auth/user/add.html')
    elif request.method == 'POST':
       # 判断是超级还是普通
        if request.POST['is_superuser'] == '1':
            ob = User.objects.create_superuser(request.POST['username'],request.POST['email'],request.POST['password'])
            
        else:
            ob = User.objects.create_user(request.POST['username'],request.POST['email'],request.POST['password'])


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
        



