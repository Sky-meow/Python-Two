# encoding:utf-8
from django.conf import settings
'''
短信管理app
functions是统一发送短信的代码
'''
default_app_config = 'sms.apps.SmsConfig'

if 'system' not in settings.INSTALLED_APPS:
    raise ImportError(
        "The sms application requires support from the system application. "
        "Make sure you have the system application enabled"
    )

if not hasattr(settings, 'AUTH_USER_MODEL') and settings.AUTH_USER_MODEL != 'system.User':
    raise ImportError(
        "The sms application requires support from the User model in system. "
        "Make sure you have the system application has the User model"
    )
