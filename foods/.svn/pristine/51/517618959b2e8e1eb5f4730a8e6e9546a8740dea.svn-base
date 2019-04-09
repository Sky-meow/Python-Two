from django.conf import settings  # 通过安全的方法引用系统配置文件
from django.urls import path, re_path, include
from customer import api
from rest_framework import routers

app_name = 'customer'

# 注册viewset类
router = routers.DefaultRouter()
router.register('', api.AddressViewSet)

urlpatterns = [
    path('get_customers', api.get_customers.as_view()),
    path('functions', api.functions()),
    re_path('^', include(router.urls))
]

# 判断api是否启用,启用则把当前的api路由添加到api的路由种
if 'api' in settings.INSTALLED_APPS:
    from api import urls
    urls.urlpatterns += urlpatterns
else:
    # 如果没有启用api,则直接把当前的路由添加到项目的主路由中
    from foods import urls
    urls.urlpatterns += urlpatterns
