# encoding:utf-8
import uuid
from django.conf import settings
from django.db import models


class Customer(models.Model):
    '''
    个人用户实体类
    可以申请成为企业用户的主账户
    可以是属于企业用户的下级用户
    也可以是独立的个人用户
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile = models.CharField(max_length=15, null=True,
                              unique=True, verbose_name=u'手机号')
    password = models.BinaryField(
        max_length=255, null=True, verbose_name=u'密码')
    name = models.CharField(null=False, max_length=100,
                            db_index=True, verbose_name=u'姓名')
    company = models.CharField(
        null=True, blank=True, max_length=100, db_index=True, verbose_name=u'公司名称')
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL,
                               db_constraint=False, blank=True, related_name='belong_to', verbose_name=u'归属于')
    store = models.ForeignKey('store.store', null=True, blank=True,
                              on_delete=models.SET_NULL, db_constraint=False, verbose_name=u'绑定项目', related_name='bind_store')
    is_buessini = models.BooleanField(default=False, verbose_name=u'是否是企业用户')
    monthly = models.BooleanField(default=False, verbose_name=u'是否允许月结')
    settlement_cycle = models.IntegerField(default=0, verbose_name='结算天数')
    openid = models.CharField(max_length=80, null=True, blank=True,
                              unique=True, db_index=True, verbose_name=u'微信唯一标识')
    enable = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        self.Name = '%s(Tel:%s)' % (self.Name, self.Mobile)
        if self.Company is None or self.Company == '':
            return self.Name
        else:
            return '公司:%s(%s)' % (self.Company, self.Name)

    class Meta:
        verbose_name = u'客户'
        verbose_name_plural = verbose_name


class Address(models.Model):
    '''
    客户送餐地址
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE,
                                 db_constraint=False, blank=True, related_name='customer_address', verbose_name=u'用户')
    contact = models.CharField(max_length=30, null=True, verbose_name=u'联系人')
    telnumber = models.CharField(
        max_length=30, null=True, verbose_name=u'联系电话')
    address = models.CharField(max_length=150, null=True, verbose_name=u'送餐地址')
    housenum = models.CharField(max_length=100, null=True, verbose_name=u'门牌号')
    point = models.CharField(max_length=30, null=True, verbose_name=u'坐标')
    is_default = models.BooleanField(default=False, verbose_name=u'是否默认')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')

    def __str__(self):
        return self.Address+self.HouseNum

    class Meta:
        verbose_name = u'送餐地址'
        verbose_name_plural = verbose_name


class WXToken(models.Model):
    '''
    保存微信返回的access_token与refresh_token
    '''
    openId = models.CharField(max_length=50, null=False, unique=True,
                              db_index=True, verbose_name=u'用户唯一标识', primary_key=True)
    access_token = models.CharField(
        max_length=200, null=True, unique=True, db_index=True, verbose_name=u'网页授权接口调用凭证')
    expires_in = models.DateTimeField(null=True, verbose_name=u'有效期到')
    refresh_token = models.CharField(
        max_length=200, null=True, unique=True, db_index=True, verbose_name=u'用户刷新access_token')
    endTime = models.DateTimeField(null=True, verbose_name=u'有效期到')


if 'store' in settings.INSTALLED_APPS:
    class BuesinessApply(models.Model):
        '''
        签约申请记录
        '''
        id = models.UUIDField(
            primary_key=True, default=uuid.uuid4, editable=False)
        store = models.ForeignKey('store.Store', null=True, blank=True,
                                  on_delete=models.SET_NULL, db_constraint=False, verbose_name=u'签约项目', related_name='apply_store')
        customer = models.ForeignKey(Customer, null=False, on_delete=models.CASCADE,
                                     db_constraint=False, blank=True, related_name='buesiness_apply', verbose_name=u'申请人')
        company = models.CharField(
            null=False, blank=True, max_length=100, db_index=True, verbose_name=u'公司名称')
        created_at = models.DateTimeField(
            auto_now_add=True, verbose_name=u'申请时间')
        is_pass = models.NullBooleanField(
            null=True, default=None, verbose_name=u'是否通过')
        settlement_cycle = models.IntegerField(default=0, verbose_name='结算天数')
        minprice = models.FloatField(default=0, verbose_name=u'签约最小金额')
        maxprice = models.FloatField(default=0, verbose_name=u'签约最大金额')

        class Meta:
            verbose_name = u'客户签约申请记录'
            verbose_name_plural = verbose_name

    if 'material' in settings.INSTALLED_APPS:
        class BussinessMats(models.Model):
            '''
            企业签约商品
            '''
            id = models.UUIDField(
                primary_key=True, default=uuid.uuid4, editable=False)
            store = models.ForeignKey('store.Store', null=True, blank=True,
                                      on_delete=models.SET_NULL, db_constraint=False, verbose_name=u'签约项目', related_name='bussiness_bind_store')
            bussiness = models.ForeignKey(
                Customer, null=False, on_delete=models.CASCADE, db_constraint=False, verbose_name=u'签约企业', related_name='bussiness_customer')
            material = models.ManyToManyField(
                'material.Material', null=True, related_name='bussiness_bind_store_material', db_constraint=False, verbose_name=u'签约商品')
            minprice = models.FloatField(default=0, verbose_name=u'签约最小金额')
            maxprice = models.FloatField(default=0, verbose_name=u'签约最大金额')
            monthly = models.BooleanField(
                default=False, verbose_name=u'是否允许月结')

            class Meta:
                verbose_name = u'企业签约'
                verbose_name_plural = verbose_name
