"""foods URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.urls import path,re_path,include
from rest_framework_swagger.views import get_swagger_view
import xadmin
xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

#加载api
from rest_framework import routers
#from apps.api.views import crypt

from apps.weixinpay import WechatAPI
router = routers.DefaultRouter()

schema_view = get_swagger_view(title='Pastebin API')
urlpatterns = []

urlpatterns = [
    re_path(r'admin/', xadmin.site.urls),
    path('WX/openId', WechatAPI.OpenIdView.as_view()),
    path('WX/auth', WechatAPI.AuthView.as_view()),
    path('WX/userInfo', WechatAPI.GetInfoView.as_view()),
    path('WX/wxsignature', WechatAPI.GetSignature.as_view()),
    re_path(r'^', include('api.urls')), #API地址
    re_path(r'WX/pay/',include('weixinpay.urls')),
    re_path(r'^ueditor/',include('DjangoUeditor.urls' )),#富文本编辑器
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.apps import apps
import os

path = os.path.join(settings.BASE_DIR, 'apps')
for app in settings.INSTALLED_APPS:
    if app != 'api':
        if apps.is_installed(app):
            app_path = os.path.join(path, app)
            if os.path.exists(app_path):
                if 'urls.py' in os.listdir(app_path):
                    urlpatterns.append(re_path(r"^%s/" % app, include(app + ".urls")))
                elif 'url.py' in os.listdir(app_path):
                    urlpatterns.append(re_path(r"^%s/" % app, include(app + ".url")))

