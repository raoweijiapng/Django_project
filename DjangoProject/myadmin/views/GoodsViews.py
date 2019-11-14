from django.shortcuts import render, reverse
from django.http import HttpResponse,JsonResponse

from . CatesViews import get_cates_all
from . UsersViews import uploads_pic
from .. models import Cates, Goods
from DjangoProject.settings import BASE_DIR
import os
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

# 商品添加 表单
def goods_add(request):
    # 获取当前所有的分类数据
    data = get_cates_all()
    # 分配数据
    context = {'catelist':data}
    # 显示一个添加的表单
    return render(request,'myadmin/goods/add.html',context)

def goods_insert(request):

  try:
      # 接收表单数据
      data = request.POST.dict()
      data.pop('csrfmiddlewaretoken')
      print(data)
      # 处理 分类对象
      data['cateid'] = Cates.objects.get(id=data['cateid'])
      # 判断是否有图片上传
      myfile = request.FILES.get('pic', None)
      if not myfile:
          return HttpResponse('<script>alert("必须上传商品图片");history.back(-1);</script>')
      # 处理  上传的文件
      data['pic_url'] = uploads_pic(myfile)

      # 执行添加
      ob = Goods(**data)
      ob.save()

      return HttpResponse('<script>alert("商品添加成功");location.href="'+reverse('myadmin_goods_index')+'";</script>')

  except:
      pass

  return HttpResponse('<script>alert("商品添加失败");history.back(-1);</script>')


def goods_index(request):
    # 获取所有的商品对象
    data = Goods.objects.all()

    # 获取搜索条件
    types = request.GET.get('types', None)
    keywords = request.GET.get('keywords', None)
    # 判断是否搜索
    if types == 'all':
        from django.db.models import Q
        data = data.filter(Q(id__contains=keywords) | Q(goodsname__contains=keywords) | Q(title__contains=keywords))
    elif types:
        search = {types + '__contains': keywords}
        data = data.filter(**search)

    # 导入分页类
    from django.core.paginator import Paginator
    # 实例化分页类，第二个参数是每页多少条
    p = Paginator(data, 6)
    # 获取当前的页码数
    pageindex = request.GET.get('page', 1)
    # 获取当前页的数据
    goodslist = p.page(pageindex)

    # 获取所有的页码
    # p.count 一共多少条
    # pages = p.page_range #迭代器(range(,))
    # pages = p.num_pages #分了多少页

    context = {'goodslist': goodslist}

    # 加载模板
    return render(request, 'myadmin/goods/index.html', context)

def goods_edit(request):
    # 接受商品id
    uid = request.GET.get('uid')
    # 获取当前会员对象
    gd = Goods.objects.get(id=uid)

    # 判断当前的请求方式
    if request.method == 'POST':

        # 判断头像是否更新
        myfile = request.FILES.get('pic', None)
        if myfile:
            # 如果有新头像上传,则先删除原头像图片,
            os.remove(BASE_DIR + gd.pic_url)
            # /static/uploads/1545033786.7237682.png
            # ./static/uploads/1545033786.7237682.png
            # /home/yc/py16/py16-project/web
            # 在上传新的头像
            gd.pic_url = uploads_pic(myfile)

        # 更新其它字段
        gd.goodsname = request.POST.get('goodsname')
        gd.title = request.POST.get('title')
        gd.price = request.POST.get('price')
        gd.goodsnum = request.POST.get('goodsnum')
        gd.goodsinfo = request.POST.get('goodsinfo')
        gd.save()
        return HttpResponse('<script>alert("更新成功");location.href="' + reverse('myadmin_goods_index') + '";</script>')

    else:
        # 显示编辑表单
        context = {'uinfo': gd}
        return render(request, 'myadmin/goods/edit.html', context)

def goods_set_status(request):
    # 通过uid获取当前商品对象
    ob = Goods.objects.get(id=request.GET.get('uid'))
    ob.status = request.GET.get('status')
    ob.save()
    return JsonResponse({'msg': '状态更新成功', 'code': 0})
