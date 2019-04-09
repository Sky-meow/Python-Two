# encoding:utf-8
from django.conf import settings
from api.views import tools
from django.urls import path, re_path, include
from .schema import SwaggerSchemaView

app_name = 'api'

urlpatterns = [
    re_path(r'^docs/', SwaggerSchemaView.as_view()),    
    re_path(r'tools/getQrcode/(.+)$', tools.getQrcode),
    re_path(r'tools/getBarcode/(.+)$', tools.getBarcode),
    re_path(r'tools/smsCaptcha/(.+)$', tools.smsCaptcha),
]

from django.apps import apps
import os

path = os.path.join(settings.BASE_DIR, 'apps')
for app in settings.INSTALLED_APPS:
    if app != 'api':
        if apps.is_installed(app):
            app_path = os.path.join(path, app)
            if os.path.exists(app_path):
                if 'api' in os.listdir(app_path) and os.path.isdir(os.path.join(app_path, 'api')):
                    dir_ = os.path.join(app_path, 'api')
                    if 'urls.py' in os.listdir(dir_):
                        urlpatterns.append(re_path(r"^%s/" % app, include(app + ".api.urls")))
                    elif 'url.py' in os.listdir(dir_):
                        urlpatterns.append(re_path(r"^%s/" % app, include(app + ".api.url")))

