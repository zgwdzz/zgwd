from django.conf.urls import url
from django.contrib import admin
from .views import index_views,user_views,cate_views,goods_views
urlpatterns = [
    #路由 
    url(r'^$', index_views.index,name='myadmin_index'),
    # 用户管理
    url(r'^vipuser/$', user_views.vipuser,name='myadmin_vipuser'),
    url(r'^adduser/$', user_views.adduser,name='myadmin_adduser'),
    url(r'^deluser/$', user_views.deluser,name='myadmin_deluser'),
    url(r'^edituser/$', user_views.edituser,name='myadmin_edituser'),
    # 重置密码
    url(r'^respwd/$', user_views.respwd,name='myadmin_respwd'),
    # 修改状态
    url(r'^changes/$', user_views.changes,name='myadmin_changes'),
    # 类别管理
    url(r'^addcate/$',cate_views.addcate,name='myadmin_addcate'),
    url(r'^catelist/$', cate_views.catelist,name='myadmin_catelist'),
    url(r'^delcate/$', cate_views.delcate,name='myadmin_delcate'),
    url(r'^editcate/$', cate_views.editcate,name='myadmin_editcate'),
    # 商品管理
    url(r'^addgoods/$', goods_views.addgoods,name='myadmin_addgoods'),
    url(r'^goodslist/$', goods_views.goodslist,name='myadmin_goodslist'),
    url(r'^goodsinsert/$', goods_views.goodsinsert,name='myadmin_goodsinsert'),
    url(r'^delgoods/$', goods_views.delgoods,name='myadmin_delgoods'),
    url(r'^editgoods/$', goods_views.editgoods,name='myadmin_editgoods'),
    # 登录 
    url(r'^login/$', index_views.login,name='myadmin_login'),
    url(r'^verifycode/$', index_views.verifycode,name='myadmin_yzm'),
    url(r'^outlogin/$', index_views.outlogin,name='myadmin_out'),










]
