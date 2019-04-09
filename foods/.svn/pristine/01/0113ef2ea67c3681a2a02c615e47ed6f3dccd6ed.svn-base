import xadmin
from sms.models import *


class SmsTemplateAdmin(object):
    list_display = ['name', 'templateId', 'key', 'content', 'enable']
    search_fields = ['name', 'templateId', 'key', 'content']
    list_filter = ['name', 'templateId', 'key', 'content', 'enable']


class SmsLogAdmin(object):
    list_display = ['key', 'content', 'sendTime', 'status', 'reason']
    search_fields = ['Mobile', 'Name', 'created_at']
    list_filter = ['key', 'content', 'sendTime', 'status', 'reason']


xadmin.site.register(SmsTemplate, SmsTemplateAdmin)  # 注册短信模板管理
xadmin.site.register(SmsLog, SmsLogAdmin)  # 注册短信发送日志管理
