# encoding:utf-8
'''
Api授权类
'''
from django.db import models
import binascii
import os
from datetime import datetime, timedelta
from django.conf import settings
import uuid
# Create your models here.


class customer_auth(models.Model):
    '''
    客户授权
    '''
    token = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    token_data = models.TextField(null=False, verbose_name=u'Token保存的缓存数据')
    expire_date = models.DateTimeField(u'有效期到', null=True)
    customer = models.OneToOneField('customer.Customer', unique=True, on_delete=models.CASCADE, db_constraint=True)


    def save(self, *args, **kwargs):
        if settings.TOKEN_EXPIRE > 0:
            self.expire_date = (
                datetime.now() + timedelta(minutes=settings.TOKEN_EXPIRE))
        return super(customer_auth, self).save(*args, **kwargs)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = u'Api授权有效期'
        verbose_name_plural = verbose_name
