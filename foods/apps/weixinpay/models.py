#encoding:utf-8

# from django.db import models

# class WXOrder(models.Model):
#     ID = models.BigAutoField(primary_key=True)
#     transaction_id = models.CharField(max_length=32,default='',null=False,verbose_name=u'微信订单号')
#     order_no = models.CharField(max_length=20, null=False,default='',db_index=True,unique=True,verbose_name=u'订单编号')
#     total_fee = models.FloatField(default=0,verbose_name=u'订单金额')
#     refund_fee = models.FloatField(default=0,verbose_name=u'退款金额')

#     class Meta:
#         verbose_name = u'微信订单'
#         verbose_name_plural = verbose_name