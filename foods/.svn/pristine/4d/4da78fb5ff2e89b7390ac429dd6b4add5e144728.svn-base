# -*- coding: utf-8 -*-

"""
微信公众号和商户平台信息配置文件
"""
from django.conf import settings

# ----------------------------------------------微信公众号---------------------------------------------- #
if settings.DEBUG:
    # 公众号appid
    APPID = 'wx9a2d5b3677f842ef'
    # 公众号AppSecret
    APPSECRET = '10e8c5e7d061b8db9d2e5127e0e37c59'
    Token = 'ec34b0dbbccd8ece98c2736d07933c56'
    EncodingAESKey = 'LOCmCeiBPBGHr1r27xynGaiGDLGRuVlOm4f9gLORzxz'
    WXH = 'gh_278e5946d10e'#微信硬件接入 安卓必须这个东西,但是...文档没有提
else:
    # 公众号appid
    APPID = 'wx9a2d5b3677f842ef'
    # 公众号AppSecret
    APPSECRET = '10e8c5e7d061b8db9d2e5127e0e37c59'

    WXH = 'gh_4cc2c72f4646' #微信硬件接入 安卓必须这个东西,但是...文档没有提

# ----------------------------------------------微信商户平台---------------------------------------------- #
# 商户id
MCH_ID = '1514211751'

API_KEY = 'A12hjom56YLp67gbfR468904de0982HD'

# ----------------------------------------------回调页面---------------------------------------------- #
# 用户授权获取code后的回调页面，如果需要实现验证登录就必须填写
# REDIRECT_URI = 'http://demo.ssspei.com/skip.html'
# PC_LOGIN_REDIRECT_URI = 'http://demo.ssspei.com/foods.html'
REDIRECT_URI = 'http://foods.ssspei.com/skip.html'
PC_LOGIN_REDIRECT_URI = 'http://foods.ssspei.com/foods.html'

defaults = {
    # 微信内置浏览器获取code微信接口
    'wechat_browser_code': 'https://open.weixin.qq.com/connect/oauth2/authorize',
    # 微信内置浏览器获取access_token微信接口
    'wechat_browser_access_token': 'https://api.weixin.qq.com/sns/oauth2/access_token',
    # 微信内置浏览器获取用户信息微信接口
    'wechat_browser_user_info': 'https://api.weixin.qq.com/sns/userinfo',
    # pc获取登录二维码接口
    'pc_QR_code': 'https://open.weixin.qq.com/connect/qrconnect',
    # pc获取登录二维码接口
    # 'pc_QR_code': 'https://api.weixin.qq.com/sns/userinfo',
    # 使用refresh_token进行刷新access_token
    'wechat_browser_refresh_token': 'https://api.weixin.qq.com/sns/oauth2/refresh_token',
    # 获取公众平台的API调用所需的access_token
    'wechat_total_access_token': 'https://api.weixin.qq.com/cgi-bin/token',
    # 获取jsapi_ticket
    'wechat_jsapi_ticket': 'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
}


SCOPE = 'snsapi_userinfo'
PC_LOGIN_SCOPE = 'snsapi_login'
STATE = ''
LANG = 'zh_CN'

PRINT = {
    'EncodingAESKey':'VBsXkw6AFUvr5PIMkVhyCIzN2LTyOU0hnJpfiTsdLly',
    'Token':'abcdefghijklmnopqrstuvwxyz123456'
}