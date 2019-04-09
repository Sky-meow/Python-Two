# encoding:utf-8
import uuid
from django.conf import settings
from django.db import models

# Create your models here.


class SmsTemplate(models.Model):
    '''
    短信模板管理
    '''
    FUNC_CHOICE = (
        (u'neworder', u'新订单提醒'),
        (u'pickup', u'派送中提醒'),
        (u'bindphone_captch', u'绑定手机验证'),
        (u'chphone_captch', '更换手机验证'),
    )
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=True, blank=True,
                            max_length=25, verbose_name='模板名称')
    templateId = models.CharField(
        null=False, max_length=50, verbose_name='短信服务模板ID')
    key = models.CharField(choices=FUNC_CHOICE, max_length=20,
                           verbose_name='短信提醒事件', db_index=True, null=True, blank=True)
    content = models.TextField(
        null=False, max_length=280, verbose_name='短信模板内容')
    enable = models.BooleanField(default=True, verbose_name='启用')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    created_by = models.ForeignKey('system.User', null=True, blank=True, on_delete=models.SET_NULL,
                                   db_constraint=False, verbose_name='创建人', related_name='smstemplate_created_by')
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name='修改时间', null=True, blank=True)
    updated_by = models.ForeignKey('system.User', null=True, blank=True, on_delete=models.SET_NULL,
                                   db_constraint=False, verbose_name='修改人', related_name='smstemplate_updated_by')

    class Meta:
        verbose_name = u'短信模板'
        verbose_name_plural = verbose_name


class SmsLog(models.Model):
    '''
    短信发送记录
    '''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    key = models.CharField(max_length=20, verbose_name='短信提醒事件')
    content = models.CharField(
        null=False, max_length=280, verbose_name='短信模板内容')
    sendTime = models.DateTimeField(
        auto_now_add=True, verbose_name='创建时间', null=True, blank=True)
    status = models.CharField(null=True, blank=True,
                              max_length=25, verbose_name='状态')
    reason = models.CharField(null=True, blank=True,
                              max_length=100, verbose_name='记录')

    class Meta:
        verbose_name = u'短信日志'
        verbose_name_plural = verbose_name
