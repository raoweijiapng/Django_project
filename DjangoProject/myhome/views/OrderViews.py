from django.shortcuts import render,reverse
from django.http import HttpResponse,Http404,JsonResponse

from myadmin.models import Cates,Goods,Cart,Users,Order,OrderInfo


# 订单确认页
def myhome_order_confirm(request):
    try:
        buy = request.GET.get('buy')
        if buy:
            goodid = request.GET.get('goodid')
            num = request.GET.get('num')
            uid = request.GET.get('uid')
            data = Cart()
            data.goodsid = Goods.objects.get(id=goodid)
            data.num = num
            data.uid = Users.objects.get(id=uid)
            data.save()
            text = Cart.objects.filter(uid=uid,goodsid=goodid,num=num)
            context = {'cartdata': text}
        else:
            # 获取选择的购物车id
            cartidstr = request.GET.get('cartids')
            cartids = cartidstr.split(',')
            print(cartids)
            # 把当前选择的购物车数据查询处理
            data = Cart.objects.filter(id__in=cartids)
            context = {'cartdata': data}

        # 加载模板
        return render(request,'myhome/order/confirm.html',context)
    except:
        pass
    return HttpResponse('<script>alert("服务器繁忙,请进入购物车结算");location.href="'+reverse('myhome_cart_index')+'";</script>')


# 订单的创建
def myhome_order_create(request):
    # 接受数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')

    # {'username': '王五', 'address': '北京市', 'cartids': '9,10', 'phone': '13701383017'}

    # 创建订单
    ob = Order()
    ob.uid = Users.objects.get(id=request.session.get('VipUser')['uid'])
    ob.username = data['username']
    ob.phone = data['phone']
    ob.address = data['address']
    ob.totalprice = 0
    ob.save()

    totalprice = 0
    # 创建订单详情
    if len(data['cartids'])>1:
        cartdata = Cart.objects.filter(id__in=data['cartids'].split(','))
        for x in cartdata:
            # 创建订单详情
            obinfo = OrderInfo()
            obinfo.orderid = ob
            obinfo.goodsid = x.goodsid
            obinfo.num = x.num
            obinfo.save()
            # 计算总价
            totalprice += x.num*x.goodsid.price
            # 删除购物车中已经下单的商品
            x.delete()
    else:
        cartdata = Cart.objects.get(id=data['cartids'])
        obinfo = OrderInfo()
        obinfo.orderid = ob
        obinfo.goodsid = cartdata.goodsid
        obinfo.num = cartdata.num
        obinfo.save()
        # 计算总价
        totalprice = cartdata.num * cartdata.goodsid.price
        # 删除购物车中已经下单的商品
        cartdata.delete()

    # 修改订单的总价
    ob.totalprice = totalprice
    ob.save()

    # 重定向到支付页面
    return HttpResponse('<script>alert("订单创建成功,请支付");location.href="'+reverse('myhome_order_pay')+'?orderid='+str(ob.id)+'"</script>')


# 订单支付
def myhome_order_pay(request):
    orderid = request.GET.get('orderid')

    return HttpResponse('请支付您的订单.订单号为:'+str(orderid))

