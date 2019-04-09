#encoding:utf-8

from django.db import models
from django.contrib.auth.models import AbstractUser 
from easy_thumbnails.fields import ThumbnailerImageField

class WeChatToken(models.Model):
    access_token = models.CharField(max_length=200,primary_key=True,null=False,unique=True,db_index=True,verbose_name=u'网页授权接口调用凭证')
    expires_in = models.DateTimeField(null=True,verbose_name=u'有效期到')

class OrderIncrement(models.Model):
    numrole = models.CharField(primary_key=True,max_length=10)
    serial = models.IntegerField(default=1)


def avatar_to(instance, filename):
    '''
    指定头像的上传地址
    '''
    from django.conf import settings
    import os
    return os.sep.join(['upload', 'avatar', 'admin', instance.id, filename])


class User(AbstractUser):
    '''
    继承系统用户表并扩展
    '''
    mobile = models.CharField(
        max_length=11, default='', null=True, blank=True, verbose_name=u'手机号')
    avatar = ThumbnailerImageField(upload_to=avatar_to, verbose_name='头像',
                               null=True, blank=True, default='')
    openId = models.CharField(max_length=50,null=True, blank=True, unique=True,db_index=True,verbose_name=u'用户唯一标识')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = u'系统用户'
        verbose_name_plural = verbose_name
