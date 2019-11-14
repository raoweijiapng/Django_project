from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse
from .. models import Order

def order_index(request):
    # 获取所有的商品对象
    data = Order.objects.all()

    # 获取搜索条件
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 判断是否搜索
    if types == 'all':
        from django.db.models import Q
        data = data.filter(Q(id__contains=keywords) | Q(username__contains=keywords) | Q(phone__contains=keywords))
    elif types:
        search = {types + '__contains': keywords}
        data = data.filter(**search)

    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分页类，第二个参数是每页多少条
    p = Paginator(data, 15)
    # 获取当前的页码数
    pageindex = request.GET.get('page', 1)
    # 获取当前页的数据
    orderslist = p.page(pageindex)

    # 获取所有的页码
    # p.count 一共多少条
    # pages = p.page_range #迭代器(range(,))
    # pages = p.num_pages #分了多少页

    context = {'orderslist': orderslist}

    # 加载模板
    return render(request, 'myadmin/order/index.html', context)

def orders_set_status(request):
    # 通过uid获取当前商品对象
    ob = Order.objects.get(id=request.GET.get('uid'))
    ob.status = request.GET.get('status')
    ob.save()
    return JsonResponse({'msg': '支付状态更新成功', 'code': 0})

def orders_set_paytype(request):
    # 通过uid获取当前商品对象
    ob = Order.objects.get(id=request.GET.get('uid'))
    ob.paytype = request.GET.get('paytype')
    ob.save()
    return JsonResponse({'msg': '支付方式状态更新成功', 'code': 0})

def myadmin_order_del(request):
    oid = request.GET.get('oid')
    # 判断当前分类下是否还有子类
    res = Order.objects.get(id=oid)
    res.delete()
    return JsonResponse({'msg': '删除成功', 'code': 0})

