# encoding:utf-8
import uuid
from django.db import models
from customer.models import *
from material.models import *
from store.models import *

# Create your models here.


class Order(models.Model):
    '''
    订单单头
    BuessiniCustomer与Customer二选一
    '''
    STATUS_CHOICES = (
        (u'new', u'新订单'),
        (u'cancel', u'已取消'),
        (u'confirm', u'已确认'),
        (u'sending', u'派送中'),
        (u'complate', u'已完成'),
    )

    ORDER_TYE_CHOICES = (
        (0, '预定订单'),
        (1, '现场订单')
    )

    PAY_TYPE = (
        (u'WeChat', u'微信支付'),
        (u'monthly', u'月结'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    increment_id = models.CharField(
        max_length=20, null=False, default='', verbose_name=u'订单编号')
    order_type = models.IntegerField(
        choices=ORDER_TYE_CHOICES, default=0, verbose_name='订单类型')
    paied = models.BooleanField(default=False, verbose_name=u'是否付款')
    paytype = models.CharField(
        choices=PAY_TYPE, max_length=15, default='WeChat', verbose_name=u'结算方式')
    customer = models.ForeignKey(Customer, db_index=True, on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='ordered_customer', db_constraint=False, verbose_name=u'下单客户')
    qty = models.IntegerField(default=0, verbose_name=u'订单总数')
    amt = models.FloatField(default=0, verbose_name=u'订单总金额')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='ordered_customer_address', db_constraint=False, verbose_name=u'送货地址')
    address_snapshot = models.CharField(
        max_length=150, null=True, blank=True, verbose_name=u'送餐地址快照')
    status = models.CharField(
        choices=STATUS_CHOICES, max_length=15, default='new', verbose_name=u'订单状态')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'下单时间')
    confirm_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name=u'确认时间')
    cancel_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name=u'取消时间')
    complate_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name=u'完成时间')
    transaction_id = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=u'支付平台交易ID')
    paied_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name=u'支付时间')
    prepayid = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=u'预支付ID')
    prepay_at = models.DateTimeField(
        default=None, null=True, blank=True, verbose_name=u'预支付时间')

    def mat_list(self):
        from .serializers import OrderItemsSerializers
        from django.utils.html import format_html
        import json
        items = obj.order_items.all().order_by('mattype')
        dic = dict()
        for item in items:
            if item.mattype_id not in dic.keys():
                dic[item.mattype_id] = {}
            dic[item.mattype_id] = dict(json.loads(
                dic[item.mattype_id]), **json.loads(item.materials))

        mattypes = obj.order_items.all().values_list('mattype', flat=True)
        string = ((['<dt>%s</dt>%s' % (mattype.name, '<dl><span>%s</span><span>%.2f</span><img src="%s" /><span>%.2f</span><span>%.2f</span></dl>' % ())
                    for key in dic[mattype.id]]) for mattype in mattypes)
        return string
        # return format_html(
        #     '<p><span>{}</span></p>\
        #     <p><span>{}</span></p>\
        #     <p><span>{}</span></p>\
        #     <p><span>{}</span></p>\
        #     <p><span>{}</span></p>\
        #     <p><span>{}</span></p>\
        #     <p><span>{}</span></p>',
        #     '身份证号 : ' + self.idcard if self.idcard is not None else '',
        #     'QQ : ' + self.qq if self.qq is not None else '',
        #     '微信号 : ' + self.wechat if self.wechat is not None else '',
        #     '电子邮件 : ' + self.email if self.email is not None else '',
        #     '年龄 : ' + str(self.age) if self.age is not None else '',
        #     '从业时间 : '+ str(self.workingtime) if self.workingtime is not None else '',
        #     '紧急联络人 : ' + self.emergencycontact if self.emergencycontact is not None else '' + ('(' + self.emergencyphone + ')' if self.emergencyphone is not None else ''),
        #     '地址 : '+ self.address if self.address is not None else ''
        # )
        # return OrderItemsSerializers(items, many=True).data
    mat_list.short_description = '商品明细'
    # 定义的字段,在xadmin中必须是只读的

    def __str__(self):
        return self.increment_id

    class Meta:
        verbose_name = u'订单'
        verbose_name_plural = verbose_name


class OrderItems(models.Model):
    '''
    订单表体
    '''
    STATUS_CHOICES = (
        ('new', '待确认'),
        ('pick-up', '已取货'),
        ('confirm', '待取货'),
        ('timeout', '已超时'),
        ('rejected', '已驳回')
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    item = models.IntegerField(default=1, verbose_name=u'项次号')
    status = models.CharField(
        choices=STATUS_CHOICES, default='confirm', max_length=50, verbose_name='状态')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=False,
                              related_name='order_items', db_constraint=False, verbose_name=u'订单')
    mattype = models.ForeignKey(MatType, on_delete=models.SET_NULL, null=True,
                                related_name='order_items_mattype', db_constraint=False, verbose_name=u'商品类别')
    materials = models.TextField(
        null=True, blank=True, verbose_name=u'预定的商品')  # JSON格式
    price = models.FloatField(default=0, verbose_name=u'菜品单价')
    qty = models.IntegerField(default=0, verbose_name=u'数量')
    amt = models.FloatField(default=0, verbose_name=u'小计')

    class Meta:
        #db_table = 'TableName'
        ordering = ('id', )   #用于表示其为一个组
        verbose_name = u'订单明细'
        verbose_name_plural = verbose_name
