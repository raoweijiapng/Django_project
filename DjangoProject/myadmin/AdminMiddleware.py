from django.shortcuts import render, reverse
from django.http import HttpResponse
import re

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        # 用户的请求路径# /myadmin/cate/index/
        path = request.path
        # 定义允许访问的路径
        arr = ['/myadmin/login/','/myadmin/dologin/','/myadmin/verifycode/']
        # 检测用户是否访问后台,并且不是进入登录页面
        if re.match('/myadmin/',path) and path not in arr:
            # 检测是否已经登录
            AdminUser = request.session.get('AdminUser',None)
            if not AdminUser:
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="'+reverse('myadmin_login')+'";</script>')

        #前台登录的中间件
        homeurl = [
            reverse('myhome_cart_add'),
            reverse('myhome_cart_index'),
            reverse('myhome_cart_del'),
            reverse('myhome_cart_clear'),
            reverse('myhome_cart_edit'),
            reverse('myhome_order_confirm'),
            reverse('myhome_order_create'),
            reverse('myhome_order_pay'),
            reverse('myhome_center_order'),

        ]

        if path in homeurl:
            # 检测是否已经登录
            VipUser = request.session.get('VipUser', None)
            if not VipUser:
                # 没有登录
                return HttpResponse('<script>alert("请先登录");location.href="' + reverse('myhome_login') + '";</script>')

        response = self.get_response(request)
        return response