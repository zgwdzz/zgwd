from django.shortcuts import render,redirect
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse,JsonResponse
from django.core.urlresolvers import reverse
from myadmin import models
# Create your views here.
def index(request):
    return render(request,'myhome/index.html')

# 登录
def myhome_login(request):
    return render(request,'myhome/login.html')
# 注册
def myhome_register(request):
    if request.method == 'GET':
        return render(request,'myhome/register.html')
    elif request.method == 'POST':
        # 接受用户的数据
        userinfo = request.POST.dict()
        # 1.判断用户是否输入信息
        if userinfo['username'] == '' or userinfo['phone'] == '' and userinfo['password'] == '':
            return HttpResponse('<script>alert("你的信息填写不完整");location.href="'+reverse("myhome_register")+'"</script>')

        # 2.判断手机号是否已经被注册
        flage = models.Users.objects.filter(phone=userinfo['phone']).count()
        if flage:
            # 如果已经存在 就返回提示信息
            return HttpResponse('<script>alert("手机号已经存在");history.back(-1)</script>')
        else:
            # 手机号可用
            # 判断验证码
            try:
                if userinfo['yzm'] == request.session['msgcode']['code'] and userinfo['phone'] == request.session['msgcode']['phone']:
                    # 存数据
                    newuser =models.Users()
                    newuser.username=userinfo['username'] 
                    newuser.phone=userinfo['phone'] 
                    newuser.password=make_password(userinfo['password'], None, 'pbkdf2_sha256')
                    newuser.save()
                    return HttpResponse('<script>alert("注册成功，请登录");location.href="'+reverse("myhome_login")+'"</script>')
                else:
                    return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')
            except:
                return HttpResponse('<script>alert("验证码错误");history.back(-1)</script>')




        

def sendmsg(request):
    
    #接口类型：互亿无线触发短信接口，支持发送验证码短信、订单通知短信等。
    #账户注册：请通过该地址开通账户http://user.ihuyi.com/register.html
    #注意事项：
    #（1）调试期间，请用默认的模板进行测试，默认模板详见接口文档；
    #（2）请使用 用户名 及 APIkey来调用接口，APIkey在会员中心可以获取；
    #（3）该代码仅供接入互亿无线短信接口参考使用，客户可根据实际需要自行编写；
      
    # import urllib2
    import urllib
    import urllib.request
    import json
    import random
    #用户名 查看用户名请登录用户中心->验证码、通知短信->帐户及签名设置->APIID
    account  = "C12884139" 
    #密码 查看密码请登录用户中心->验证码、通知短信->帐户及签名设置->APIKEY
    password = "efcf5e25515b46c7094d7ce36e983fcc"
    mobile = request.GET.get('phone')
    # 随机验证码
    code = str(random.randint(10000,99999))
    # 把验证码存入session
    request.session['msgcode'] = {'code':code,'phone':mobile}
    text = "您的验证码是："+code+"。请不要把验证码泄露给其他人。"
    data = {'account': account, 'password' : password, 'content': text, 'mobile':mobile,'format':'json' }
    req = urllib.request.urlopen(
        url= 'http://106.ihuyi.com/webservice/sms.php?method=Submit',
        data= urllib.parse.urlencode(data).encode('utf-8')
    )
    content =req.read()
    res = json.loads(content.decode('utf-8'))
    print(res)
    # return HttpResponse(res)
    return JsonResponse(res)