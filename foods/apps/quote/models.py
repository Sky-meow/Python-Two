from django.db import models
from customer.models import Customer
from store.models import Store
from material.models import Material

# Create your models here.
class Quote(models.Model):
    '''
    购物车
    '''
    id       = models.BigAutoField(primary_key=True)
    project  = models.ForeignKey(Store,null=False,on_delete=models.CASCADE,db_constraint = False,verbose_name=u'项目/食堂')
    customer = models.ForeignKey(Customer,null=False,on_delete=models.CASCADE,db_constraint = False,verbose_name=u'客户')    

    class Meta:
        verbose_name = u'购物车'
        verbose_name_plural = verbose_name

class QuoteItem(models.Model):
    '''
    购物车明细
    '''
    id       = models.BigAutoField(primary_key=True)
    quote    = models.ForeignKey(Quote,on_delete=models.CASCADE,db_constraint=False,verbose_name=u'购物车')
    material = models.ForeignKey(Material,on_delete=models.CASCADE,db_constraint=False,verbose_name=u'商品')
    qty      = models.FloatField(default = 1,verbose_name=u'数量')

    class Meta:
        verbose_name = u'购物车明细'
        verbose_name_plural = verbose_name

