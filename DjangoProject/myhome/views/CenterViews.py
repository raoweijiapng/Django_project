from django.shortcuts import render
from django.http import HttpResponse,Http404,JsonResponse

from myadmin.models import Cates,Goods,Cart,Users,Order,OrderInfo

# 个人中心 视图

# 我的订单
def myhome_center_order(request):

    # 获取当前用户的所有订单
    orderdata = Order.objects.filter(uid=request.session.get('VipUser')['uid'])
    totalprice = 0
    for x in  orderdata:
        orderinfo = x.orderinfo_set.all()
        for y in orderinfo:
            totalprice += y.goodsid.price*y.num
        x.totalprice = totalprice

    # 分配数据
    context = {'orderdata':orderdata}

    # 加载模板
    return render(request,'myhome/center/order.html',context)