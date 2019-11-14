from django.db import models

# Create your models here.

# 定义会员模型
class Users(models.Model):
    nikename = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=100)
    # phone = models.CharField(max_length=11,unique=True)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    pic_url = models.CharField(max_length=100)
    SEX_CHOICES = (
        (0, '女'),
        (1, '男'),
    )
    sex = models.CharField(max_length=1,null=True,choices=SEX_CHOICES)
    # 0 正常  1禁用  2 删除 ....
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)


# 商品分类模型
class Cates(models.Model):
    name = models.CharField(max_length=20)
    pid = models.IntegerField()
    path = models.CharField(max_length=50)
    ''' 无限分类
        id  name    pid  path
        1    服装     0    0,
        2    男装     1    0,1,
        3    西服     2    0,1,2,
        4    休闲西服  3    0,1,2,3,
        5    女装     1    0,1,
        6    裙子     5    0,1,5,
        7    超短裙    6   0,1,5,6,
    '''

# 商品模型
class Goods(models.Model):
    # id 所属分类,商品名,图片,添加时间,销量
    cateid = models.ForeignKey(to="Cates", to_field="id", on_delete=models.CASCADE)
    goodsname = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    goodsnum = models.IntegerField()
    pic_url = models.CharField(max_length=255)
    goodsinfo = models.TextField()
    ordernum =  models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    # 0 新品,1热卖,2推荐,3下架
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

# 购物车 模型
class Cart(models.Model):
    # id  用户 uid   商品 goodsid 数量 num
    uid = models.ForeignKey(to="Users", to_field="id",on_delete=models.CASCADE)
    goodsid = models.ForeignKey(to="Goods", to_field="id",on_delete=models.CASCADE)
    num = models.IntegerField()

# 订单
class Order(models.Model):
    uid = models.ForeignKey(to="Users", to_field="id",on_delete=models.CASCADE)
    username = models.CharField(max_length=20)
    phone = models.CharField(max_length=11)
    address = models.CharField(max_length=255)
    totalprice = models.FloatField()
    # 0 未支付, 1已支付, 2已发货  3已收货  4已评价  5取消 ...
    status = models.IntegerField(default=0)
    # 0 支付宝  1 微信 2 银联  3 其它  4货到付款...
    paytype = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    paytime = models.DateTimeField(null=True)


# 订单详情
class OrderInfo(models.Model):
    orderid = models.ForeignKey(to="Order", to_field="id",on_delete=models.CASCADE)
    goodsid = models.ForeignKey(to="Goods", to_field="id",on_delete=models.CASCADE)
    num = models.IntegerField()

'''
# 订单
    id订单号 uid用户 收货人,收货地址,收货电话,总价,状态 支付方式 ,下单时间,支付时间
    100011       189     
# 订单详情
    orderid   goodsid   num  price购买时的单价
    100011     12       1
    100011     18       3
'''

