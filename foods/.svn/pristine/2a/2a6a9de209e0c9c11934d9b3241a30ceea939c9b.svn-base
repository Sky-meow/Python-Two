#encoding:utf-8
from .views import *
from django.urls import path,re_path,include

app_name = 'WXpay'
urlpatterns = [
    path('pay',Pay.as_view()),
    path('getWxPayParams',getWxPayParams.as_view()),
    path('queryOrder',QueryWXOrder.as_view()),
    path('refund',Refund.as_view()),
]